#!/usr/bin/python

"""
This example shows how to create a simple network and
how to create docker containers (based on existing images)
to it.
"""

import SDN_MininetUtils

from mininet.net import Mininet;
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link
from mininet.node import Controller, OVSSwitch

from SDN_Docker import DockerHost

def topology():

    "Create a network with some docker containers acting as hosts."

    net = Mininet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    info('*** Adding docker containers\n')
    _volumes = [];
    _volumes.append("/bin:/bin");
    _volumes.append("/sbin:/sbin");
    _volumes.append("/lib:/lib");
    _volumes.append("/include:/include");
    _volumes.append("/usr/bin:/usr/bin");
    _volumes.append("/usr/sbin:/usr/sbin");
    _volumes.append("/usr/lib:/usr/lib");
    _volumes.append("/usr/include:/usr/include");
    _volumes.append("/usr/local/bin:/usr/local/bin");
    _volumes.append("/usr/local/sbin:/usr/local/sbin");
    _volumes.append("/usr/local/lib:/usr/local/lib");
    _volumes.append("/usr/local/include:/usr/local/include");
    _volumes.append("/home/souvikdas95:/home/souvikdas95");
    d1 = net.addHost('d1', ip='10.0.0.251', cls=DockerHost, dimage="ubuntu:latest", volumes = _volumes, cpu_shares=20);
    d2 = net.addHost('d2', ip='10.0.0.252', cls=DockerHost, dimage="ubuntu:latest", volumes = _volumes, cpu_shares=20);
    d3 = net.addHost('d3', ip='10.0.0.253', cls=DockerHost, dimage="ubuntu:latest", volumes = _volumes, cpu_shares=20);

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2', cls=OVSSwitch)
    s3 = net.addSwitch('s3')

    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(s1, d1)
    net.addLink(h2, s2)
    net.addLink(d2, s2)
    net.addLink(s1, s2)
    #net.addLink(s1, s2, cls=TCLink, delay="100ms", bw=1, loss=10)
    # try to add a second interface to a docker container
    net.addLink(d2, s3, params1={"ip": "11.0.0.254/8"})
    net.addLink(d3, s3)
    net.addLink(s2, s3)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()