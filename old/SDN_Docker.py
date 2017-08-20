#!/usr/bin/python

import os
import pty
import re
import select
import docker
import json

from subprocess import Popen, check_output
from mininet.log import info, error, warn, debug
from mininet.util import isShellBuiltin
from mininet.node import Host
from re import findall

class DockerHost ( Host ):
    """Node that represents a docker container.
    This part is inspired by:
    http://techandtrains.com/2014/08/21/docker-container-as-mininet-host/
    We use the docker-py client library to control docker.
    """

    def __init__(
            self, name, dimage, dcmd=None, **kwargs):
        """
        Creates a Docker container as Mininet host.
        Resource limitations based on CFS scheduler:
        * cpu.cfs_quota_us: the total available run-time within a period (in microseconds)
        * cpu.cfs_period_us: the length of a period (in microseconds)
        (https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt)
        Default Docker resource limitations:
        * cpu_shares: Relative amount of max. avail CPU for container
            (not a hard limit, e.g. if only one container is busy and the rest idle)
            e.g. usage: d1=4 d2=6 <=> 40% 60% CPU
        * cpuset: Bind containers to CPU 0 = cpu_1 ... n-1 = cpu_n
        * mem_limit: Memory limit (format: <number>[<unit>], where unit = b, k, m or g)
        * memswap_limit: Total limit = memory + swap
        All resource limits can be updated at runtime! Use:
        * updateCpuLimits(...)
        * updateMemoryLimits(...)
        """
        self.dimage = dimage
        self.dnameprefix = "mn"
        self.dcmd = dcmd if dcmd is not None else "/bin/bash"
        self.dc = None  # pointer to the container
        self.dcinfo = None
        self.did = None # Id of running container
        #  let's store our resource limits to have them available through the
        #  Mininet API later on
        defaults = { 'cpu_quota': -1,
                     'cpu_period': None,
                     'cpu_shares': None,
                     'cpuset_cpus': None,
                     'mem_limit': None,
                     'memswap_limit': None,
                     'environment': {},
                     'volumes': [],  # use ["/home/user1/:/mnt/vol2:rw"]
                     'publish_all_ports': True,
                     'port_bindings': {},
                     }
        defaults.update( kwargs )

        # keep resource in a dict for easy update during container lifetime
        self.resources = dict(
            cpu_quota=defaults['cpu_quota'],
            cpu_period=defaults['cpu_period'],
            cpu_shares=defaults['cpu_shares'],
            cpuset_cpus=defaults['cpuset_cpus'],
            mem_limit=defaults['mem_limit'],
            memswap_limit=defaults['memswap_limit']
        )

        self.volumes = defaults['volumes']
        self.environment = {} if defaults['environment'] is None else defaults['environment']
        self.environment.update({"PS1": chr(127)})  # CLI support
        self.publish_all_ports = defaults['publish_all_ports']
        self.port_bindings = defaults['port_bindings']

        # setup docker client
        self.dcli = docker.APIClient(base_url='unix://var/run/docker.sock')

        # pull image if it does not exist
        self._check_image_exists(dimage, True)

        debug("Created docker container object %s\n" % name)
        debug("image: %s\n" % str(self.dimage))
        debug("dcmd: %s\n" % str(self.dcmd))
        debug("kwargs: %s\n" % str(kwargs))

        # call original Node.__init__
        Host.__init__(self, name, **kwargs)


    def startShell( self, mnopts=None ):
        if self.dc is None:
            # creats host config for container
            # see: https://docker-py.readthedocs.org/en/latest/hostconfig/
            hc = self.dcli.create_host_config(
                network_mode=None,
                privileged=True,  # we need this to allow mininet network setup
                binds=self.volumes,
                publish_all_ports=self.publish_all_ports,
                port_bindings=self.port_bindings,
                mem_limit=self.resources.get('mem_limit'),
                cpuset_cpus=self.resources.get('cpuset_cpus'),
            )
            # create new docker container
            self.dc = self.dcli.create_container(
                name="%s.%s" % (self.dnameprefix, self.name),
                image=self.dimage,
                command=self.dcmd,
                stdin_open=True,  # keep container open
                tty=True,  # allocate pseudo tty
                environment=self.environment,
                #network_disabled=True,  # docker stats breaks if we disable the default network
                host_config=hc,
                labels=['com.containernet'],
                volumes=[self._get_volume_mount_name(v) for v in self.volumes if self._get_volume_mount_name(v) is not None],
                hostname=self.name
            )
            # start the container
            self.dcli.start(self.dc)
            debug("Docker container %s started\n" % self.name)
            # fetch information about new container
            self.dcinfo = self.dcli.inspect_container(self.dc)
            self.did = self.dcinfo.get("Id")

            # let's initially set our resource limits
            self.update_resources(**self.resources)
            # self.updateCpuLimit(cpu_quota=self.resources.get('cpu_quota'),
            #                     cpu_period=self.resources.get('cpu_period'),
            #                     cpu_shares=self.resources.get('cpu_shares'),
            #                     )
            # self.updateMemoryLimit(mem_limit=self.resources.get('mem_limit'),
            #                        memswap_limit=self.resources.get('memswap_limit')
            #                        )

        # use a new shell to connect to container to ensure that we are not
        # blocked by initial container command
        cmd = ["docker",
               "exec",
               "-it",
               "%s.%s" % (self.dnameprefix, self.name),
               "/bin/bash"
               ]
        # Spawn a shell subprocess in a pseudo-tty, to disable buffering
        # in the subprocess and insulate it from signals (e.g. SIGINT)
        # received by the parent
        master, slave = pty.openpty()
        self.shell = self._popen( cmd, stdin=slave, stdout=slave, stderr=slave,
                                  close_fds=False )
        # original Mininet membervars set in startShell method
        self.stdin = os.fdopen( master, 'rw' )
        self.stdout = self.stdin
        self.pid = self._get_pid()
        self.pollOut = select.poll()
        self.pollOut.register( self.stdout )
        self.outToNode[ self.stdout.fileno() ] = self
        self.inToNode[ self.stdin.fileno() ] = self
        self.execed = False
        self.lastCmd = None
        self.lastPid = None
        self.readbuf = ''
        self.waiting = False
        #self.output = ''

        # fix container environment (sentinel chr(127))
        # we cannot set the sentinel in the docker shell here
        # setting PS1 breaks the python docker api (update_container hangs...)
        # the sentinel is added after each executed cmd in sendCmd
        #self.cmd('export PS1="\\127"')

    def _get_volume_mount_name(self, volume_str):
        """ Helper to extract mount names from volume specification strings """
        parts = volume_str.split(":")
        if len(parts) < 3:
            return None
        return parts[1]

    def terminate( self ):
        """ Stop docker container """
        self.dcli.stop(self.dc, timeout=1)
        # also remove the container
        # TODO this should be optional later
        try:
            self.dcli.remove_container(self.dc, force=True, v=True)
        except docker.errors.APIError as e:
            info("Warning: API error during container removal.\n")
        self.cleanup()

    def sendCmd( self, *args, **kwargs ):
        """Send a command, followed by a command to echo a sentinel,
           and return without waiting for the command to complete.
           args: command and arguments, or string
           printPid: print command's PID? (False)"""
        assert self.shell# and not self.waiting
        printPid = kwargs.get( 'printPid', False )
        # Allow sendCmd( [ list ] )
        if len( args ) == 1 and isinstance( args[ 0 ], list ):
            cmd = args[ 0 ]
        # Allow sendCmd( cmd, arg1, arg2... )
        elif len( args ) > 0:
            cmd = args
        # Convert to string
        if not isinstance( cmd, str ):
            cmd = ' '.join( [ str( c ) for c in cmd ] )
        if not re.search( r'\w', cmd ):
            # Replace empty commands with something harmless
            cmd = 'echo -n'
        self.lastCmd = cmd
        # if a builtin command is backgrounded, it still yields a PID
        if len( cmd ) > 0 and cmd[ -1 ] == '&':
            # print ^A{pid}\n so monitor() can set lastPid
            cmd += ' printf "\\001%d\\012" $! '
        elif printPid and not isShellBuiltin( cmd ):
            cmd = 'mnexec -p ' + cmd

        # for Docker hosts, we need to add the sentinel ourselves
        #output = self.cmd(*args, **kwargs)
        #self.output = output + chr(127)
        cmd = cmd + " ;printf \\\\177 " + '\n'
        self.write( cmd )
        self.lastPid = None
        self.waiting = True

    def monitor( self, timeoutms=None, findPid=True ):
        """Monitor and return the output of a command.
           Set self.waiting to False if command has completed.
           timeoutms: timeout in ms or None to wait indefinitely
           findPid: look for PID from mnexec -p"""

        # for Docker hosts, this is a patch, to make the containernet CLI work
        self.waitReadable( timeoutms )
        data = self.read( 1024 )
        #data = self.output
        pidre = r'\[\d+\] \d+\r\n'
        # Look for PID
        marker = chr( 1 ) + r'\d+\r\n'
        if findPid and chr( 1 ) in data:
            # suppress the job and PID of a backgrounded command
            if re.findall( pidre, data ):
                data = re.sub( pidre, '', data )
            # Marker can be read in chunks; continue until all of it is read
            while not re.findall( marker, data ):
                data += self.read( 1024 )
            markers = re.findall( marker, data )
            if markers:
                self.lastPid = int( markers[ 0 ][ 1: ] )
                data = re.sub( marker, '', data )
        # Look for sentinel/EOF
        if len( data ) > 0 and data[ -1 ] == chr( 127 ):
            self.waiting = False
            data = data[ :-1 ]
        elif chr( 127 ) in data:
            self.waiting = False
            data = data.replace( chr( 127 ), '' )
            # remove last line (contains container prompt) and replace by clean line
            data = data[:data.rfind('\n')] + '\n'
        # Suppress original cmd input (will otherwise be printed in docker TTY)
        if len( data ) > 0:
            data = data.replace(self.lastCmd, '').lstrip()
            # remove first line (if it contains the print sentinel command)
            first_line = data.split('\n', 1)[0]
            if ";printf \\\\177" in first_line:
                data = data.split('\n', 1)[1]
            # check if output contains prompt:
            promptre = r'root@.*:.*#'
            prompt_found = re.findall(promptre, data)
            if prompt_found:
                #data = data[:data.rfind(prompt_found[0])] + '\n'
                data = data + '\n'

        return data

    def popen( self, *args, **kwargs ):
        """Return a Popen() object in node's namespace
           args: Popen() args, single list, or string
           kwargs: Popen() keyword args"""
        # Tell mnexec to execute command in our cgroup
        mncmd = ["docker",
                 "exec",
                 "-it",
                 "%s.%s" % (self.dnameprefix, self.name)
                 ]
        return Host.popen( self, *args, mncmd=mncmd, **kwargs )

    def pexec( self, cmd, *args, **kwargs ):
        """Execute a command using popen
           returns: out, err, exitcode
           FIXME: Popen with Docker containers does not work.
           No idea why!
           We fake it with normal Node.cmd() -> this hangs with certain containers, no idea why!
           We use the docker api recommended way to execute commands inside containers
           """
        out = self.cmd(cmd)
        err = ""
        exitcode = 0
        return out, err, exitcode

    def cmd(self, *args, **kwargs ):

        # Allow sendCmd( [ list ] )
        if len(args) == 1 and isinstance(args[0], list):
            cmd = args[0]
        # Allow sendCmd( cmd, arg1, arg2... )
        elif len(args) > 0:
            cmd = args
        # Convert to string
        if not isinstance(cmd, str):
            cmd = ' '.join([str(c) for c in cmd])

        # check if container is still running
        container_list = self.dcli.containers(filters={"id": self.did, "status": "running"})
        if len(container_list) == 0:
            debug("container {0} not found, cannot execute command: {1}".format(self.name, cmd))
            self.waiting = False
            return ''

        exec_dict = self.dcli.exec_create(self.dc, cmd, privileged=True)
        out = self.dcli.exec_start(exec_dict)
        #info("cmd: {0} \noutput:{1}".format(cmd, out))
        self.waiting = False
        return out

    def _get_pid(self):
        state = self.dcinfo.get("State", None)
        if state:
            return state.get("Pid", -1)
        return -1

    def _check_image_exists(self, imagename, pullImage=False):
        # split tag from repository if a tag is specified
        if ":" in imagename:
            repo, tag = imagename.split(":")
        else:
            repo = imagename
            tag = "latest"

        if self._image_exists(repo, tag):
            return True

        # image not found
        if pullImage:
            if self._pull_image(repo, tag):
                info('*** Download of "%s:%s" successful\n' % (repo, tag))
                return True
        # we couldn't find the image
        return False

    def _image_exists(self, repo, tag):
        """
        Checks if the repo:tag image exists locally
        :return: True if the image exists locally. Else false.
        """
        # filter by repository
        images = self.dcli.images(repo)

        imageName = "%s:%s" % (repo, tag)

        for image in images:
            if 'RepoTags' in image:
                if imageName in image['RepoTags']:
                    return True

        return False

    def _pull_image(self, repository, tag):
        """
        :return: True if pull was successful. Else false.
        """
        try:
            info('*** Image "%s:%s" not found. Trying to load the image. \n' % (repository, tag))
            info('*** This can take some minutes...\n')

            message = ""
            for line in self.dcli.pull(repository, tag, stream=True):
                # Collect output of the log for enhanced error feedback
                message = message + json.dumps(json.loads(line), indent=4)

        except:
            error('*** error: _pull_image: %s:%s failed.' % (repository, tag)
                  + message)
        if not self._image_exists(repository, tag):
            error('*** error: _pull_image: %s:%s failed.' % (repository, tag)
                  + message)
            return False
        return True

    def update_resources(self, **kwargs):
        """
        Update the container's resources using the docker.update function
        re-using the same parameters:
        Args:
           blkio_weight
           cpu_period, cpu_quota, cpu_shares
           cpuset_cpus
           cpuset_mems
           mem_limit
           mem_reservation
           memswap_limit
           kernel_memory
           restart_policy
        see https://docs.docker.com/engine/reference/commandline/update/
        or API docs: https://docker-py.readthedocs.io/en/stable/api.html#module-docker.api.container
        :return:
        """

        self.resources.update(kwargs)
        # filter out None values to avoid errors
        resources_filtered = {res:self.resources[res] for res in self.resources if self.resources[res] is not None}
        info("{1}: update resources {0}\n".format(resources_filtered, self.name))
        self.dcli.update_container(self.dc, **resources_filtered)


    def updateCpuLimit(self, cpu_quota=-1, cpu_period=-1, cpu_shares=-1, cores=None):
        """
        Update CPU resource limitations.
        This method allows to update resource limitations at runtime by bypassing the Docker API
        and directly manipulating the cgroup options.
        Args:
            cpu_quota: cfs quota us
            cpu_period: cfs period us
            cpu_shares: cpu shares
            cores: specifies which cores should be accessible for the container e.g. "0-2,16" represents
                Cores 0, 1, 2, and 16
        """
        # see https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt

        # also negative values can be set for cpu_quota (uncontrained setting)
        # just check if value is a valid integer
        if isinstance(cpu_quota, (int, long)):
            self.resources['cpu_quota'] = self.cgroupSet("cfs_quota_us", cpu_quota)
        if cpu_period >= 0:
            self.resources['cpu_period'] = self.cgroupSet("cfs_period_us", cpu_period)
        if cpu_shares >= 0:
            self.resources['cpu_shares'] = self.cgroupSet("shares", cpu_shares)
        if cores:
            self.dcli.update_container(self.dc, cpuset_cpus=cores)
            # quota, period ad shares can also be set by this line. Usable for future work.

    def updateMemoryLimit(self, mem_limit=-1, memswap_limit=-1):
        """
        Update Memory resource limitations.
        This method allows to update resource limitations at runtime by bypassing the Docker API
        and directly manipulating the cgroup options.
        Args:
            mem_limit: memory limit in bytes
            memswap_limit: swap limit in bytes
        """
        # see https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt
        if mem_limit >= 0:
            self.resources['mem_limit'] = self.cgroupSet("limit_in_bytes", mem_limit, resource="memory")
        if memswap_limit >= 0:
            self.resources['memswap_limit'] = self.cgroupSet("memsw.limit_in_bytes", memswap_limit, resource="memory")


    def cgroupSet(self, param, value, resource='cpu'):
        """
        Directly manipulate the resource settings of the Docker container's cgrpup.
        Args:
            param: parameter to set, e.g., cfs_quota_us
            value: value to set
            resource: resource name: cpu
        Returns: value that was set
        """
        cmd = 'cgset -r %s.%s=%s docker/%s' % (
            resource, param, value, self.did)
        debug(cmd + "\n")
        try:
            check_output(cmd, shell=True)
        except:
            error("Problem writing cgroup setting %r\n" % cmd)
            return
        nvalue = int(self.cgroupGet(param, resource))
        if nvalue != value:
            error('*** error: cgroupSet: %s set to %s instead of %s\n'
                  % (param, nvalue, value))
        return nvalue

    def cgroupGet(self, param, resource='cpu'):
        """
        Read cgroup values.
        Args:
            param: parameter to read, e.g., cfs_quota_us
            resource: resource name: cpu / memory
        Returns: value
        """
        cmd = 'cgget -r %s.%s docker/%s' % (
            resource, param, self.did)
        try:
            return int(check_output(cmd, shell=True).split()[-1])
        except:
            error("Problem reading cgroup info: %r\n" % cmd)
            return -1