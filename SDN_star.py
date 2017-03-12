#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

import sys, os, threading, time;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

# Base Directory
BASE_DIR = os.path.dirname(os.path.realpath(__file__));

# Add BASE_DIR to PYTHONPATH
sys.path.append(BASE_DIR);

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Node
from mininet.util import waitListening
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import OVSLink
from mininet.link import OVSIntf
from mininet.link import TCLink
from mininet.link import TCIntf
from mininet.clean import Cleanup

from SDN_config import *;

# Create Mininet Instance
setLogLevel('info');
net = Mininet(topo = None, controller = None, build = False, waitConnected = True);

# Connect to Controller
info('*** Connecting to controller\n');
net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6653);

# Create Switches
info('*** Creating switches (Open vSwitch w/ OpenFlow13)\n');
sw_src = net.addSwitch('s0', cls = OVSSwitch, protocols = 'OpenFlow13', inband = False); # Source Switch
noise_swlist = [];
for i in range(NOISE_SWITCHES):
    noise_swlist.append(net.addSwitch('s' + str(i + 1), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False));
#sw_dst = net.addSwitch('s' + str(i + 2), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False); # Destination Switch

# Create Switch - Switch Links (Bus Topology)
info('*** Creating Switch - Switch Links (Bus Topology)\n');
#swlink_src = net.addLink(sw_src, noise_swlist[0], cls = TCLink, Intf = TCIntf, fast = False); # Link to Source Switch
noise_swlinklist = [];
for i in range(NOISE_SWITCHES):
    noise_swlinklist.append(net.addLink(sw_src, noise_swlist[i], cls = TCLink, Intf = TCIntf, fast = False));
#swlink_dst = net.addLink(noise_swlist[i + 1], sw_dst, cls = TCLink, Intf = TCIntf, fast = False); # Link to Destination Switch

# Declare IP Pool
iter_ip = IP2INT('10.0.0.128'); # Starting Address

# Create Hosts
info('*** Creating hosts\n');
h_src = net.addHost('h0', ip = INT2IP(iter_ip)); # Source Host
iter_ip += 1;
noise_hlist = [];
for i in range(NOISE_SWITCHES):
    noise_hlist.insert(i, []);
    for j in range(NOISE_HOSTS_PER_SWITCH):
        noise_hlist[i].append(net.addHost('h' + str(i * NOISE_HOSTS_PER_SWITCH + j + 1), ip = INT2IP(iter_ip)));
        iter_ip += 1;
h_dst = net.addHost('h' + str(i * NOISE_HOSTS_PER_SWITCH + j + 1 + 1), ip = INT2IP(iter_ip)); # Destination Host 
iter_ip += 1;

# Create Host - Switch Links (Star Topology)
info('*** Creating Host - Switch Links (Star Topology)\n');
hlink_src = net.addLink(h_src, sw_src, cls = TCLink, Intf = TCIntf, fast = False); # Link from Source Host to Source Switch
noise_hlinklist = [];
for i in range(NOISE_SWITCHES):
    noise_hlinklist.insert(i, []);
    for j in range(NOISE_HOSTS_PER_SWITCH):
        noise_hlinklist[i].append(net.addLink(noise_swlist[i], noise_hlist[i][j], cls = TCLink, Intf = TCIntf, fast = False));
#hlink_dst = net.addLink(sw_dst, h_dst, cls = TCLink, Intf = TCIntf, fast = False); # Link from Destination Switch to Destination Host

# Start Network
info('*** Starting Network\n');
net.start();

# Print Required Host Information
info('********************\n');
info('Source Host: ' + h_src.name + ' (' + h_src.IP(intf = h_src.defaultIntf()) + ')\n');
#info('Destination Host: ' + h_dst.name + ' (' + h_dst.IP(intf = h_dst.defaultIntf()) + ')\n');
info('********************\n');

# Configure Traffic Control on Switch - Switch Interfaces
info('*** Configuring Traffic Control on Switch - Switch Interfaces\n');
setLogLevel('error');
#swlink_src.intf1.config(bw = LINK_SPEED);
#swlink_src.intf2.config(bw = LINK_SPEED);
for i in range(NOISE_SWITCHES - 1):
    noise_swlinklist[i].intf1.config(bw = LINK_SPEED);
    noise_swlinklist[i].intf2.config(bw = LINK_SPEED);
#swlink_dst.intf1.config(bw = LINK_SPEED);
#swlink_dst.intf2.config(bw = LINK_SPEED);
setLogLevel('info');

# Configure Traffic Control on Host - Switch Interfaces
info('*** Configuring Traffic Control on Host - Switch Interfaces\n');
setLogLevel('error');
hlink_src.intf1.config(bw = LINK_SPEED);
hlink_src.intf2.config(bw = LINK_SPEED);
for i in range(NOISE_SWITCHES):
    for j in range(NOISE_HOSTS_PER_SWITCH):
        noise_hlinklist[i][j].intf1.config(bw = LINK_SPEED);
        noise_hlinklist[i][j].intf2.config(bw = LINK_SPEED);
#hlink_dst.intf1.config(bw = LINK_SPEED);
#hlink_dst.intf2.config(bw = LINK_SPEED);
setLogLevel('info');

# Configure Host Default Routes
info('*** Configuring Host Default Routes\n');
h_src.setDefaultRoute(h_src.defaultIntf());
for i in range(NOISE_SWITCHES):
    for j in range(NOISE_HOSTS_PER_SWITCH):
        noise_hlist[i][j].setDefaultRoute(noise_hlist[i][j].defaultIntf());
h_dst.setDefaultRoute(h_dst.defaultIntf());

def STREAM(STREAM_SRC, STREAM_DST):
	# Start Noise
	info('*** Starting Noise . . .\n');
	for i in range(NOISE_SWITCHES):
		for j in range(NOISE_HOSTS_PER_SWITCH):
			noise_hlist[i][j].cmd(	'cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
								 	'./noise_udp ' + str(NOISE_SOCKET_PORT) + ' ' + str(NOISE_PACKET_PAYLOAD_SIZE) + ' ' + str(NOISE_PACKET_DELAY) + ' '
									'&>' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'noise_udp.log &');

	# Initialize Packet Capture
	info('*** Initializing Packet Capture . . .\n');
	h_dst.cmd(	'cd \'' + BASE_DIR + '\' && '
				'touch \'output' + os.path.sep + 'pcap' + os.path.sep + 'destination_host.pcap\' && '
				'tshark -i \'' + h_dst.defaultIntf().name + '\' -f \'host ' + STREAM_IP + ' and port ' + str(STREAM_PORT) + '\' -w \'output' + os.path.sep + 'pcap' + os.path.sep + 'destination_host.pcap\' '
				'&>output' + os.path.sep + 'logs' + os.path.sep + 'tshark_destination.log &');
	h_src.cmd(	'cd \'' + BASE_DIR + '\' && '
				'touch \'output' + os.path.sep + 'pcap' + os.path.sep + 'source_host.pcap\' && '
				'tshark -i \'' + h_src.defaultIntf().name + '\' -f \'host ' + STREAM_IP + ' and port ' + str(STREAM_PORT) + '\' -w \'output' + os.path.sep + 'pcap' + os.path.sep + 'source_host.pcap\' '
				'&>output' + os.path.sep + 'logs' + os.path.sep + 'tshark_source.log &');

	# Sleep for 15 Seconds
	info('*** Wait 10 Seconds for Network to Settle . . .\n');
	time.sleep(10);

	# Start Streaming
	info('*** Preparing Stream Recorder . . .\n');
	h_dst.cmd(	'cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
				'java -jar \'recordVLC.jar\' \'' + STREAM_IP + '\' \'' + str(STREAM_PORT) + '\' \'' + STREAM_DST + '\' '
				'&>' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'recordVLC.log &');
		
	# Sleep for 3 Seconds
	time.sleep(3);

	info('*** Starting Stream Server . . .\n');
	h_src.cmd(	'cd \'' + BASE_DIR + os.path.sep + 'target' + '\' && '
				'java -jar \'streamVLC.jar\' \'' + STREAM_IP + '\' \'' + str(STREAM_PORT) + '\' \'' + STREAM_SRC + '\' '
				'&>' + os.path.pardir + os.path.sep + 'output' + os.path.sep + 'logs' + os.path.sep + 'streamVLC.log &');
		
	info('*** Streaming Successfully Started!\n');

# Custom Class for CLI
class CustomCLI(CLI):
	def do_stream(self, _line):
		argv = _line.split();
		if len(argv) > 0:
			if os.path.isabs(argv[0]):
				arg1 = argv[0];
			else:
				arg1 = BASE_DIR + os.path.sep + argv[0];
		else:
			arg1 = BASE_DIR + os.path.sep + 'samples/sample1.avi';
		if len(argv) > 1:
			if os.path.isabs(argv[1]):
				arg2 = argv[1];
			else:
				arg2 = BASE_DIR + os.path.sep + argv[1];
		else:
			arg2 = BASE_DIR + os.path.sep + 'output/recording/sample1.ts';
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

