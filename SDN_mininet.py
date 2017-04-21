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

# Make Directories Save (Create if not exists)
def makedirs_s(s):
	if os.path.exists(s) is False:
		os.makedirs(s);

# Tag & Make Directories
TARGET_DIR = BASE_DIR + os.path.sep + 'target';
makedirs_s(TARGET_DIR);
OUTPUT_DIR = BASE_DIR + os.path.sep + 'output';
makedirs_s(OUTPUT_DIR);

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

def STREAM(STREAM_SRC):
	# Prepare Stream Output Directory
	info('\n*** Preparing Stream Output Directories . . . ');
	SOURCE_FILENAME = os.path.split(STREAM_SRC)[1];
	_SOURCE_SPLIT = os.path.splitext(SOURCE_FILENAME);
	V_NAME = _SOURCE_SPLIT[0];
	V_EXT = _SOURCE_SPLIT[1];
	version = 1;
	STREAM_DESTDIR = OUTPUT_DIR + os.path.sep + V_NAME;
	while os.path.exists(STREAM_DESTDIR + '_v' + str(version)) is True:
		version = version + 1;
	STREAM_DESTDIR = STREAM_DESTDIR + '_v' + str(version);
	makedirs_s(STREAM_DESTDIR);
	LOGS_DIR = STREAM_DESTDIR + os.path.sep + 'logs';
	makedirs_s(LOGS_DIR);
	PCAP_DIR = STREAM_DESTDIR + os.path.sep + 'pcap';
	makedirs_s(PCAP_DIR);
	PSNR_DIR = STREAM_DESTDIR + os.path.sep + 'psnr';
	makedirs_s(PSNR_DIR);
	REC_DIR = STREAM_DESTDIR + os.path.sep + 'rec';
	makedirs_s(REC_DIR);

	# Draw Frame# Source Video
	info('\n*** Drawing FPS . . . ');
	source_host.cmd('ffmpeg -i \'' + STREAM_SRC + '\' '
					'-vf \'drawtext=fontfile=Arial.ttf: text=%{n}: x=0: y=0: fontcolor=white: box=1: boxcolor=0x00000099\' '
					'-y \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'ffmpeg_drawtext' +'.log\' 2>&1');

	# Generate SDP
	info('\n*** Generating SDP . . . ');
	source_host.cmd('ffmpeg -fflags +genpts -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\' '
					'> \'' + STREAM_DESTDIR + os.path.sep + V_NAME + '.sdp\' '
					'2> \'' + LOGS_DIR + os.path.sep + 'sdp.log\'');

	# Initialize Source Packet Capture
	info('\n*** Initializing Source Packet Capture . . . ');
	source_host.cmd('touch \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' && '
					'tshark -i \'' + source_host.defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' '
					'&> \'' + LOGS_DIR + os.path.sep + 'tshark_source' + '.log\' 2>&1 &');

	# Initialize Destination Packet Capture
	info('\n*** Initializing Destination Packet Capture . . . ');
	for i in range(DESTINATION_COUNT):
		dest_host_list[i].cmd(	'touch \'' + PCAP_DIR + os.path.sep + 'destination_host_' + str(i) + '.pcap\' && '
								'tshark -i \'' + dest_host_list[i].defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'destination_host_' + str(i) + '.pcap\' '
								'&> \'' + LOGS_DIR + os.path.sep + 'tshark_destination_' + str(i) + '.log\' 2>&1 &');

	# Start Noise
	info('\n*** Starting Noise . . . ');
	for i in range(1, SWITCH_COUNT * HOST_COUNT_PER_SWITCH):
		if host_list[i] not in dest_host_list:
			host_list[i].cmd(	'cd \'' + TARGET_DIR + '\' && '
								'java -jar \'NoiseUDP.jar\' \'' + str(NOISE_PORT) + '\' \'' + str(NOISE_PACKET_PAYLOAD_SIZE) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
								'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');

	# Wait for 10 Seconds
	info('\n*** Wait 10 Seconds for Network to Settle . . . ');
	time.sleep(10);

	# Prepare Stream Recorders
	info('\n*** Preparing Stream Recorders . . . ');
	record_args_init =(	'ffmpeg -protocol_whitelist file,udp,rtcp,rtp '
						'-i \'' + STREAM_DESTDIR + os.path.sep + V_NAME + '.sdp\' -c copy -y ');
	def _record(_dest_host, _record_args):
		_dest_host.cmd(_record_args);
	thread_record_list = [];
	for i in range(DESTINATION_COUNT):
		record_args_end =(	'\'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
							'> \'' + LOGS_DIR + os.path.sep + 'recorder_' + str(i) + '.log\' 2>&1');
		t = threading.Thread(target=_record, args=(dest_host_list[i], record_args_init + record_args_end));
		t.start();
		thread_record_list.append(t);
	time.sleep(max(5, DESTINATION_COUNT));

	# Start Streamer
	info('\n*** Starting Streamer . . . ');
	stream_args =(	'ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'streamer.log\' 2>&1');
	def _stream(_source_host, _stream_args):
		_source_host.cmd(_stream_args);
	thread_stream = threading.Thread(target=_stream, args=(source_host, stream_args));
	thread_stream.start();

	# Wait for Stream Completion
	thread_stream.join();
	info('\n*** Streaming Completed . . . ');
	for thread_record in thread_record_list:
		thread_record.join();
	info('\n*** Recording Completed . . . ');

	# Calculate PSNR for each Recording
	info('\n*** Calculating PSNR . . . ');
	for i in range(DESTINATION_COUNT):
		dest_host_list[i].cmd(	'ffmpeg -i \'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
								'-vf \"movie=\'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\', psnr=stats_file=\'' + PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt\'\" '
								'-f rawvideo -y /dev/null '
								'> \'' + LOGS_DIR + os.path.sep + 'rec_' + str(i) + '_psnr' + '.log\' 2>&1');

	info('\n*** Streaming Successfully Completed! ');

# Custom Class for CLI
class CustomCLI(CLI):
	def do_stream(self, _line):
		argv = _line.split();
		if len(argv) > 0 and os.path.isfile(argv[0]) is True:
			arg = os.path.abspath(argv[0]);
		else:
			info('*** Invalid Path!\n');
			return;
		t = threading.Thread(target = STREAM, args = (arg, ));
		t.start();

# Switch to CLI
CustomCLI(net);

# Stop Network
info('*** Stopping Network\n');
net.stop();

# Cleanup
info('*** Cleaning Up\n');
Cleanup.cleanup();
