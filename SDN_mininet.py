#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

import sys, os, threading, time, math, random;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

# Base Directory
BASE_DIR = os.path.dirname(os.path.realpath(__file__));

# Add BASE_DIR to PYTHONPATH
sys.path.append(BASE_DIR);

# Mininet Imports
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel, info;
from mininet.node import Node;
from mininet.util import waitListening;
from mininet.node import OVSSwitch, Controller, RemoteController;
from mininet.link import OVSLink;
from mininet.link import OVSIntf;
from mininet.link import TCLink;
from mininet.link import TCIntf;
from mininet.clean import Cleanup;

# Import Configuration
from SDN_config import *;

# Create Mininet Instance
setLogLevel('info');
net = Mininet(topo = None, controller = None, build = False, waitConnected = True);

# Connect to Controller
info('*** Connecting to controller\n');
net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6653, ipBase = '10.0.0.128');

# Declare IP Pool
info('*** Declaring IP Pool\n');
iter_ip = IP2INT('10.0.0.128'); # Starting Address

# Create Switches
info('*** Creating switches (Open vSwitch w/ OpenFlow13)\n');
switch_list = [];
for i in range(SWITCH_COUNT):
    sid = i + 1;
    switch_list.append(net.addSwitch('s' + str(sid), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False));

# Create Hosts
info('*** Creating hosts\n');
switch_host_list = [];
host_list = []
for i in range(SWITCH_COUNT):
    switch_host_list.append([]);
    for j in range(HOST_COUNT_PER_SWITCH):
        hid = (i * HOST_COUNT_PER_SWITCH + j) + 1;
        h = net.addHost('h' + str(hid), ip = INT2IP(iter_ip));
        switch_host_list[i].append(h);
        host_list.append(h);
        iter_ip += 1;

# Create Switch - Switch Links
info('*** Creating Switch - Switch Links\n');
switch_switch_link_list = []
if TOPOLOGY_TYPE == 1:
    for i in range(SWITCH_COUNT - 1):
        switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[i + 1], cls = TCLink, Intf = TCIntf, fast = False));
elif TOPOLOGY_TYPE == 2:
    for i in range(SWITCH_COUNT - 1):
        switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[i + 1], cls = TCLink, Intf = TCIntf, fast = False));
    switch_switch_link_list.append(net.addLink(switch_list[SWITCH_COUNT - 1], switch_list[0], cls = TCLink, Intf = TCIntf, fast = False));
elif TOPOLOGY_TYPE == 3:
    for i in range(SWITCH_COUNT - 1):
        for j in range(i + 1, SWITCH_COUNT):
            switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[j], cls = TCLink, Intf = TCIntf, fast = False));
elif TOPOLOGY_TYPE == 4:
    pass; # Nothing to do with 1 Switch :V

# Create Switch - Host Links
info('*** Creating Switch - Host Links\n');
switch_host_link_list = [];
for i in range(SWITCH_COUNT):
	switch_host_link_list.append([]);
	for j in range(HOST_COUNT_PER_SWITCH):
		switch_host_link_list[i].append(net.addLink(switch_list[i], switch_host_list[i][j], cls = TCLink, Intf = TCIntf, fast = False));

# Start Network
info('*** Starting Network\n');
net.start();

# Print Required Source Destination Information
info('********************\n');
source_host = host_list[0];
info('*** Source Host: ' + source_host.name + ' (' + source_host.IP(intf = source_host.defaultIntf()) + ')\n');
dest_host_list = random.sample(host_list[1::], DESTINATION_COUNT);
info('*** Destination Hosts: \n');
for i in range(DESTINATION_COUNT):
    info('*** ' + dest_host_list[i].name + ' (' + dest_host_list[i].IP(intf = dest_host_list[i].defaultIntf()) + ')\n');
info('********************\n');

# Configure Traffic Control on Switch - Switch Interfaces
if TOPOLOGY_TYPE != 4:
    info('*** Configuring Traffic Control on Switch - Switch Interfaces\n');
    setLogLevel('error');
    for i in range(len(switch_switch_link_list)):
        switch_switch_link_list[i].intf1.config(bw = SWITCH_LINK_SPEED);
        switch_switch_link_list[i].intf2.config(bw = SWITCH_LINK_SPEED);
    setLogLevel('info');

# Configure Traffic Control on Switch - Host Interfaces
info('*** Configuring Traffic Control on Switch - Host Interfaces\n');
setLogLevel('error');
for i in range(SWITCH_COUNT):
	for j in range(HOST_COUNT_PER_SWITCH):
		switch_host_link_list[i][j].intf1.config(bw = HOST_LINK_SPEED);
		switch_host_link_list[i][j].intf2.config(bw = HOST_LINK_SPEED);
setLogLevel('info');

# Configure Host Default Routes
info('*** Configuring Host Default Routes\n');
for i in range(SWITCH_COUNT * HOST_COUNT_PER_SWITCH):
    host_list[i].setDefaultRoute(host_list[i].defaultIntf());

def STREAM(STREAM_SRC, STREAM_DST):
	# Initialize Packet Capture
	info('\n*** Initializing Packet Capture . . .\n');
	source_host.cmd('cd \'' + BASE_DIR + '\' && '
					'touch \'output' + os.path.sep + 'pcap' + os.path.sep + 'source_host.pcap\' && '
					'tshark -i \'' + source_host.defaultIntf().name + '\' -f \'host ' + str(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'output' + os.path.sep + 'pcap' + os.path.sep + 'source_host.pcap\' '
					'&> \'output' + os.path.sep + 'logs' + os.path.sep + 'tshark_source.log\' 2>&1 &');
	for i in range(DESTINATION_COUNT):
		dest_host_list[i].cmd(	'cd \'' + BASE_DIR + '\' && '
								'touch \'output' + os.path.sep + 'pcap' + os.path.sep + 'destination_host_' + str(i) + '.pcap\' && '
								'tshark -i \'' + dest_host_list[i].defaultIntf().name + '\' -f \'host ' + str(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'output' + os.path.sep + 'pcap' + os.path.sep + 'destination_host_' + str(i) + '.pcap\' '
								'&> \'output' + os.path.sep + 'logs' + os.path.sep + 'tshark_destination_' + str(i) + '.log\' 2>&1 &');
	
	# Start Noise
	info('*** Starting Noise . . .\n');
	for i in range(1, SWITCH_COUNT * HOST_COUNT_PER_SWITCH):
		if host_list[i] not in dest_host_list:
			host_list[i].cmd(	'cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
								'java -jar \'NoiseUDP.jar\' \'' + str(NOISE_PORT) + '\' \'' + str(NOISE_PACKET_PAYLOAD_SIZE) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
								'&> \'' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'noise_udp.log\' 2>&1 &');
	
	# Sleep for 10 Seconds
	info('*** Wait 10 Seconds for Network to Settle . . .\n');
	time.sleep(10);
	
	# Prepare Stream Recorders
	info('*** Preparing Stream Recorders . . .\n');
	for i in range(DESTINATION_COUNT):
		dest_host_list[i].cmd(	'cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
								'java -jar \'recordVLC.jar\' \'' + str(STREAM_IP) + '\' \'' + str(STREAM_PORT) + '\' \'' + STREAM_DST + os.path.sep + 'rec_' + str(i) + '.ts\' '
								'&> \'' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'recordVLC_' + str(i) + '.log\' 2>&1 &');
	
	# Sleep for 3 Seconds
	time.sleep(3);

	# Draw Frame# Source Video
	info('*** Preparing Stream Content . . .\n');
	MOD_SOURCE_FILENAME = 'mod_' + os.path.split(STREAM_SRC)[1];
	source_host.cmd('ffmpeg -i \'' + STREAM_SRC + '\' '
					'-vf \'drawtext=fontfile=Arial.ttf: text=%{n}: x=0: y=0: fontcolor=white: box=1: boxcolor=0x00000099\' '
					'-y \'' + STREAM_DST + os.path.sep + MOD_SOURCE_FILENAME + '\' '
					'&> \'' + BASE_DIR + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'ffmpeg_drawtext' +'.log\' 2>&1 &');

	# Start Stream Server
	info('*** Starting Stream Server . . .\n');
	source_host.cmd('cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
					'java -jar \'streamVLC.jar\' \'' + str(STREAM_IP) + '\' \'' + str(STREAM_PORT) + '\' \'' + STREAM_DST + os.path.sep + MOD_SOURCE_FILENAME + '\' '
					'&> \'' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'streamVLC.log\' 2>&1 &');
		
	info('*** Streaming Successfully Started!\n');

# Custom Class for CLI
class CustomCLI(CLI):
	def do_stream(self, _line):
		argv = _line.split();
		if len(argv) > 0 and os.path.isfile(arg1) is True:
			arg1 = os.path.abspath(argv[0]);
		else:
			arg1 = os.path.abspath(BASE_DIR + os.path.sep + 'samples' + os.path.sep + 'sample1.avi');
		if len(argv) > 1:
			if os.path.isdir(arg2) is False:
				os.makedirs(arg2, mode = 0777);
			arg2 = os.path.abspath(argv[1]);
		else:
			arg2 = os.path.abspath(BASE_DIR + os.path.sep + 'output' + os.path.sep + 'videos');
		t = threading.Thread(target = STREAM, args = (arg1, arg2));
		t.start();

# Switch to CLI
CustomCLI(net);

# Stop Network
info('*** Stopping Network\n');
net.stop();

# Cleanup
info('*** Cleaning Up\n');
Cleanup.cleanup();

