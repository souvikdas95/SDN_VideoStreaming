#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

import os
import sys
import struct, socket

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

IP2INT = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: socket.inet_ntoa(struct.pack('!I', n));              	# Integer to IP Address

MTU = 1492;			# Maximum Transmission Unit (Bytes)
OVERHEAD = 52;		# 18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes

NOISE_SWITCHES = 4;             				# No. of Noise Switches (>= 0).
NOISE_HOSTS_PER_SWITCH = 4;     				# No. of Hosts per Noise Switch (>= 0).
NOISE_SOCKET_PORT = 65535;      				# Source/Destination Port to be used for Noise Packets  (1024-65535). Note: Avoid using port 5555

NOISE_DATA_RATE = 32 * 1024;										# Data Rate (in bps)
NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;							# Size of Noise Packet (in Bytes) per NOISE_PACKET_DELAY
NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);	# Delay b/w Consecutive Noise Packets (in Milliseconds).

LINK_SPEED = 1;     # Link Speed / Interface Speed on all Switches and Hosts (in Mbps) (1-1000)

BASE_DIR = os.path.dirname(os.path.realpath(__file__));		# Directory for Program Files

STREAM_SRC = BASE_DIR + '/examples/media.avi';		# Source Media (Streaming)
STREAM_DST = BASE_DIR + '/examples/recording.ts';	# Destination Media (Recording)

if __name__ == '__main__':
    setLogLevel('info');

    # Create Mininet Instance
    net = Mininet(topo = None, controller = None, build = False);

    # Connect to Controller
    info('*** Connecting to controller\n');
    net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6653);

    # Create Switches
    info('*** Creating switches (Open vSwitch w/ OpenFlow13)\n');
    sw_src = net.addSwitch('s0', cls = OVSSwitch, protocols = 'OpenFlow13', inband = False); # Source Switch
    noise_swlist = [];
    for i in range(NOISE_SWITCHES):
        noise_swlist.append(net.addSwitch('s' + str(i + 1), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False));
    sw_dst = net.addSwitch('s' + str(i + 2), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False); # Destination Switch

    # Create Switch - Switch Links (Bus Topology)
    info('*** Creating Switch - Switch Links (Bus Topology)\n');
    swlink_src = net.addLink(sw_src, noise_swlist[0], cls = TCLink, Intf = TCIntf, fast = False); # Link to Source Switch
    noise_swlinklist = [];
    for i in range(NOISE_SWITCHES - 1):
        noise_swlinklist.append(net.addLink(noise_swlist[i], noise_swlist[i + 1], cls = TCLink, Intf = TCIntf, fast = False));
    swlink_dst = net.addLink(noise_swlist[i + 1], sw_dst, cls = TCLink, Intf = TCIntf, fast = False); # Link to Destination Switch

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
    hlink_dst = net.addLink(sw_dst, h_dst, cls = TCLink, Intf = TCIntf, fast = False); # Link from Destination Switch to Destination Host

    # Start Network
    info('*** Starting Network\n');
    net.start();

    # Print Required Host Information
    info('********************\n');
    info('Source Host: ' + h_src.name + ' (' + h_src.IP(intf = h_src.defaultIntf()) + ')\n');
    info('Destination Host: ' + h_dst.name + ' (' + h_dst.IP(intf = h_dst.defaultIntf()) + ')\n');
    info('********************\n');

    # Configure Traffic Control on Switch - Switch Interfaces
    info('*** Configuring Traffic Control on Switch - Switch Interfaces\n');
    setLogLevel('error');
    swlink_src.intf1.config(bw = LINK_SPEED);
    swlink_src.intf2.config(bw = LINK_SPEED);
    for i in range(NOISE_SWITCHES - 1):
        noise_swlinklist[i].intf1.config(bw = LINK_SPEED);
        noise_swlinklist[i].intf2.config(bw = LINK_SPEED);
    swlink_dst.intf1.config(bw = LINK_SPEED);
    swlink_dst.intf2.config(bw = LINK_SPEED);
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
    hlink_dst.intf1.config(bw = LINK_SPEED);
    hlink_dst.intf2.config(bw = LINK_SPEED);
    setLogLevel('info');

    # Configure Host Default Routes
    info('*** Configuring Host Default Routes\n');
    h_src.setDefaultRoute(h_src.defaultIntf());
    for i in range(NOISE_SWITCHES):
        for j in range(NOISE_HOSTS_PER_SWITCH):
            noise_hlist[i][j].setDefaultRoute(noise_hlist[i][j].defaultIntf());
    h_dst.setDefaultRoute(h_dst.defaultIntf());

    # Start Noise
    info('*** Starting Noise . . .\n');
    for i in range(NOISE_SWITCHES):
        for j in range(NOISE_HOSTS_PER_SWITCH):
            noise_hlist[i][j].cmd(	'cd \'' + BASE_DIR + '\' && '
            					 	'./noise_udp ' + str(NOISE_SOCKET_PORT) + ' ' + str(NOISE_PACKET_PAYLOAD_SIZE) + ' ' + str(NOISE_PACKET_DELAY) + ' '
        							'&>/dev/null &');

    # Initialize Packet Capture
    info('*** Initializing Packet Capture . . .\n');
    h_dst.cmd(	'cd \'' + BASE_DIR + '\' && '
    			'touch \'rtp_record.pcap\' && '
    			'tshark -i \'' + h_dst.defaultIntf().name + '\' -f \'host 234.0.0.1 and port 5555\' -w \'rtp_record.pcap\' '
    			'&>/dev/null &');
    h_src.cmd(	'cd \'' + BASE_DIR + '\' && '
    			'touch \'rtp_server.pcap\' && '
    			'tshark -i \'' + h_src.defaultIntf().name + '\' -f \'host 234.0.0.1 and port 5555\' -w \'rtp_server.pcap\' '
    			'&>/dev/null &');

    # Start Streaming
    info('*** Starting Streaming . . .\n');
    h_dst.cmd(	'cd \'' + BASE_DIR + '\' && '
    			'java -jar \'rtp_record.jar\' \'' + STREAM_DST + '\' '
    			'&>/dev/null &');
    h_src.cmd(	'cd \'' + BASE_DIR + '\' && '
    			'java -jar \'rtp_server.jar\' \'' + STREAM_SRC + '\' '
    			'&>/dev/null &');
    
    # Switch to CLI
    CLI(net);

    # Stop Network
    info('*** Stopping Network\n');
    net.stop();

    # Cleanup
    info('*** Cleaning Up\n');
    Cleanup.cleanup();
