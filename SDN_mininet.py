#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

import sys, os, threading, time, math, random, csv;

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
# TARGET_DIR = BASE_DIR + os.path.sep + 'target';
# makedirs_s(TARGET_DIR);
OUTPUT_DIR = BASE_DIR + os.path.sep + 'output';
makedirs_s(OUTPUT_DIR);
SAP_DIR = BASE_DIR + os.path.sep + 'SAP';

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

# IP-INT conversion methods
IP2INT = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: socket.inet_ntoa(struct.pack('!I', n));              	# Integer to IP Address

# Stream Default Configuration
MTU = 1492; # Maximum Transmission Unit (Bytes)
OVERHEAD = 52;  # Protocol Overhead (18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes)
DESTINATION_COUNT = 1;
STREAM_IP = '234.0.0.1';
STREAM_PORT = 5555;
NOISE_PORT = 65535;
NOISE_DATA_RATE = 32 * 1024;
NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);
SAP_PORT = 49160;
NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;	# Ensure Full Utilization of Packet

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
switch_count = 0;
for i in range(SWITCH_COUNT):
    switch_count += 1;
    switch_list.append(net.addSwitch('s' + str(switch_count), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False,
    					failMode = 'standalone' if (USE_STP == True) else 'secure',
    					stp = USE_STP));

# Create Hosts
info('*** Creating hosts\n');
switch_host_list = [];
host_list = []
host_count_in_switch = HOST_COUNT_PER_SWITCH;
host_count = 0;
for i in range(SWITCH_COUNT):
	switch_host_list.append([]);
	if TOPOLOGY_TYPE == 5:
		host_count_in_switch = random.randint(0, HOST_COUNT_PER_SWITCH);
	for j in range(host_count_in_switch):
		host_count += 1;
		h = net.addHost('h' + str(host_count), ip = INT2IP(iter_ip));
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
elif TOPOLOGY_TYPE == 5:
	neighbor = {};
	for i in range(SWITCH_COUNT - 1):
		if neighbor.has_key(switch_list[i]) == False:
			neighbor[switch_list[i]] = set();
		for j in range(i + 1, SWITCH_COUNT):
			if neighbor.has_key(switch_list[j]) == False:
				neighbor[switch_list[j]] = set();
			if bool(random.getrandbits(1)) == True:
				switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[j], cls = TCLink, Intf = TCIntf, fast = False));
				neighbor[switch_list[i]].add(switch_list[j]);
				neighbor[switch_list[j]].add(switch_list[i]);
	conn_comp_list = [];
	switch_set = set(switch_list);
	while switch_set:
		sw = switch_set.pop();
		group_set = {sw};
		queue_list = [sw];
		while queue_list:
			sw = queue_list.pop(0);
			neighbor_set = neighbor[sw];
			neighbor_set.difference_update(group_set);
			switch_set.difference_update(neighbor_set);
			group_set.update(neighbor_set);
			queue_list.extend(neighbor_set);
		conn_comp_list.append(group_set);
	# for i in range(len(conn_comp_list)):
	# 	info("Component #" + str(i + 1) + ": ");
	# 	jlist = list(conn_comp_list[i]);
	# 	for j in range(len(jlist)):
	# 		info(jlist[j].name + ", ");
	# 	print("\n");
	for i in range(len(conn_comp_list) - 1):
		rand_comp_item1 = random.sample(conn_comp_list[i], 1)[0];
		rand_comp_item2 = random.sample(conn_comp_list[i + 1], 1)[0];
		switch_switch_link_list.append(net.addLink(rand_comp_item1, rand_comp_item2, cls = TCLink, Intf = TCIntf, fast = False));

# Create Switch - Host Links
info('*** Creating Switch - Host Links\n');
switch_host_link_list = [];
for i in range(SWITCH_COUNT):
	switch_host_link_list.append([]);
	for j in range(len(switch_host_list[i])):
		switch_host_link_list[i].append(net.addLink(switch_list[i], switch_host_list[i][j], cls = TCLink, Intf = TCIntf, fast = False));

# Start Network
info('*** Starting Network\n');
net.start();

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
	for j in range(len(switch_host_link_list[i])):
		switch_host_link_list[i][j].intf1.config(bw = HOST_LINK_SPEED);
		switch_host_link_list[i][j].intf2.config(bw = HOST_LINK_SPEED);
setLogLevel('info');

# Configure Host Default Routes
info('*** Configuring Host Default Routes\n');
for i in range(len(host_list)):
    host_list[i].setDefaultRoute(host_list[i].defaultIntf());

def STREAM(STREAM_SRC):
	# Delay & Print
	time.sleep(0.1);
	sys.stdout.flush();
	info('\n');
	
	# Global Declarations
	global BASE_DIR;
	global OUTPUT_DIR;
	global SAP_DIR;
	global DESTINATION_COUNT;
	global STREAM_IP;
	global STREAM_PORT;
	global NOISE_PORT;
	global NOISE_DATA_RATE;
	global NOISE_PACKET_DELAY;
	global SAP_PORT;
	global NOISE_PACKET_PAYLOAD_SIZE;
	
	# Print Required Source Destination Information
	info('\n********************\n');
	source_host = host_list[0];
	info('*** Source Host: ' + source_host.name + ' (' + source_host.IP(intf = source_host.defaultIntf()) + ')\n');
	if DESTINATION_COUNT > len(host_list) - 1:
		DESTINATION_COUNT = len(host_list) - 1;
	dest_host_list = random.sample(host_list[1::], DESTINATION_COUNT);
	info('*** Destination Hosts: \n');
	for i in range(DESTINATION_COUNT):
		info('*** ' + dest_host_list[i].name + ' (' + dest_host_list[i].IP(intf = dest_host_list[i].defaultIntf()) + ')\n');
	info('********************\n');
	
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
	SDP_DIR = STREAM_DESTDIR + os.path.sep + 'sdp';
	makedirs_s(SDP_DIR);

	# Draw Frame# Source Video
	info('\n*** Drawing Frames . . . ');
	source_host.cmd('ffmpeg -i \'' + STREAM_SRC + '\' '
					'-vf \'drawtext=fontfile=Arial.ttf: text=%{n}: x=0: y=0: fontcolor=white: box=1: boxcolor=0x00000099\' '
					'-y \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'ffmpeg_drawtext' +'.log\' 2>&1');

	# Calculate Source Frame Count
	info('\n*** Calculating Source Frame Count . . . ');
	try:
		frame_count_source = long(source_host.cmd(	'ffprobe -v error -count_frames -select_streams v:0 -show_entries '
													'stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 '
													'-i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\''));
	except ValueError:
		info('\n*** Error: Reading Source Frames Failed!');
		return;

	# Generate SDP
	info('\n*** Generating SDP . . . ');
	source_host.cmd('ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -sdp_file \'' + SDP_DIR + os.path.sep + V_NAME + '_source.sdp\' -t 0 '
					'-f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'sdp.log\' 2>&1');
	
	# Initiate SAP
	info('\n*** Initiating SAP . . . ');
	source_host.cmd('cd \'' + SAP_DIR + '\' && '
					'python SAP_server.py '
					'\'' + source_host.IP(intf = source_host.defaultIntf()) + '\' '
					'\'' + str(SAP_PORT) + '\' '
					'\'' + SDP_DIR + os.path.sep + V_NAME + '_source.sdp\' '
					'&> \'' + LOGS_DIR + os.path.sep + 'SAP_server.log\' 2>&1 &');
	sap_client_command_args_init = 	'cd \'' + SAP_DIR + '\' && python SAP_client.py ';
	def _sap_client_command(_dest_host, _sap_client_command_args):
		_dest_host.cmd(_sap_client_command_args);
	thread_sap_client_list = [];
	for i in range(DESTINATION_COUNT):
		sap_client_command_args_end = (	'\'' + source_host.IP(intf = source_host.defaultIntf()) + '\' '
										'\'' + str(SAP_PORT) + '\' '
										'\'' + SDP_DIR + os.path.sep + V_NAME + '_destination_' + str(i) + '.sdp\' '
										'> \'' + LOGS_DIR + os.path.sep + 'SAP_server.log\' 2>&1');
		t = threading.Thread(target=_sap_client_command, args=(dest_host_list[i], sap_client_command_args_init + sap_client_command_args_end));
		t.start();
		thread_sap_client_list.append(t);
	for thread_sap_client in thread_sap_client_list:
		thread_sap_client.join();
	info('\n*** SAP Completed . . . ');

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
	for i in range(1, len(host_list)):
		if host_list[i] not in dest_host_list:
			host_list[i].cmd(	'cd \'' + BASE_DIR + '\' && '
								'python \'Noise_UDP.py\' \'' + str(NOISE_PORT) + '\' \'' + str(NOISE_PACKET_PAYLOAD_SIZE) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
								'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');

	# Wait for 15 Seconds
	info('\n*** Wait 15 Seconds for Network to Settle . . . ');
	time.sleep(15);

	# Prepare Stream Recorders
	info('\n*** Preparing Stream Recorders . . . ');
	record_args_init = 'ffmpeg -protocol_whitelist file,udp,rtcp,rtp ';
	def _record(_dest_host, _record_args):
		_dest_host.cmd(_record_args);
	thread_record_list = [];
	for i in range(DESTINATION_COUNT):
		record_args_end =(	'-i \'' + SDP_DIR + os.path.sep + V_NAME + '_destination_' + str(i) + '.sdp\' -c copy -y '
							'\'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
							'> \'' + LOGS_DIR + os.path.sep + 'recorder_' + str(i) + '.log\' 2>&1');
		t = threading.Thread(target=_record, args=(dest_host_list[i], record_args_init + record_args_end));
		t.start();
		thread_record_list.append(t);
	time.sleep(max(5, DESTINATION_COUNT));

	# Start Streamer
	stream_args =(	'ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'streamer.log\' 2>&1');
	def _stream(_source_host, _stream_args):
		_source_host.cmd(_stream_args);
	thread_stream = threading.Thread(target=_stream, args=(source_host, stream_args));
	thread_stream.start();
	info('\n*** Streaming Started . . . ');

	# Wait for Stream Completion
	thread_stream.join();
	info('\n*** Streaming Completed . . . ');
	info('\n*** Waiting for Record Completion . . . ');
	for thread_record in thread_record_list:
		thread_record.join();
	info('\n*** Recording Completed . . . ');
	time.sleep(1);

	# Process PSNR for each Recording
	info('\n*** Processing PSNR Results . . . ');
	time.sleep(1);
	rec_avg_psnr_list = [];
	frame_count_dest = [];
	for i in range(DESTINATION_COUNT):
		dest_host_list[i].cmd(	'ffmpeg -i \'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
								'-vf \"movie=\'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\', psnr=stats_file=\'' + PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt\'\" '
								'-f rawvideo -y /dev/null '
								'> \'' + LOGS_DIR + os.path.sep + 'rec_' + str(i) + '_psnr' + '.log\' 2>&1');
		time.sleep(1);
		try:
			with open(PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt', 'r') as f:
				pass;
		except IOError:
			with open(PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt', 'w') as f:
				pass;
		with open(PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt', 'r+') as f:
			content = f.readlines();
			avg_mseavg = 0;
			frame_count = 0;
			for line in content:
				text = line.split(' ');
				frame_count += 1;
				try:
					mseavg = float(text[1].split(':')[1]);
				except ValueError:
					mseavg = sys.float_info.max;
				avg_mseavg += mseavg;
			if frame_count == 0:
				avg_mseavg = sys.float_info.max;
				avg_psnr = 0.0;
			else:
				avg_mseavg = avg_mseavg / frame_count;
				if avg_mseavg == 0:
					avg_psnr = float('inf'); # Make sure to not use this value for calculation anywhere!
				else:
					avg_psnr = 10 * math.log10(255 * 255 / avg_mseavg);	# Assuming BitDepth is fixed at 8-bit
			rec_avg_psnr_list.append(avg_psnr);
			frame_count_dest.append(frame_count);
		
	# Process Packets Send/Received
	info('\n*** Processing PCAP Results . . . ');
	time.sleep(1);
	try:
		packets_sent = source_host.cmd(	'tshark -r \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' '
											'-q -z io,phs | sed -n \'7,7p\' | cut -d \" \" -f 40 | cut -d \":\" -f 2').split('\n');
		if isinstance(packets_sent[-1], int):
			packets_sent = int(packets_sent[-1]);
		else:
			packets_sent = int(packets_sent[-2]);
	except ValueError:
		packets_sent = -1; # error
	packets_recv_list = [];
	for i in range(DESTINATION_COUNT):
		time.sleep(1);
		try:
			packets_recv = dest_host_list[i].cmd(	'tshark -r \'' + PCAP_DIR + os.path.sep + 'destination_host_' + str(i) + '.pcap\' '
														'-q -z io,phs | sed -n \'7,7p\' | cut -d \" \" -f 40 | cut -d \":\" -f 2').split('\n');
			if isinstance(packets_recv[-1], int):
				packets_recv = int(packets_recv[-1]);
			else:
				packets_recv = int(packets_recv[-2]);
		except ValueError:
			packets_recv = -1; # error
		packets_recv_list.append(packets_recv);
	
	# Retrieve Noise Rate
	info('\n*** Retrieving Noise Rate . . . ');
	time.sleep(1);
	try:
		with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'r') as f:
			pass;
	except IOError:
		with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'w') as f:
			pass;
	with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'r+') as f: 
		content = f.readlines();
		noise_rate = 0.0;
		for line in content:
			text = line.split(' ');
			if text[0] == 'DATA_RATE':
				try:
					noise_rate = float(text[1]);
				except ValueError:
					noise_rate = -1;
				break;
	
	# Create Report
	info('\n*** Generating Report . . . ');
	fieldnames = [	'ID',
					'Topology',
					'Switch#',
					'Hosts#',
					'Sw-Sw LinkSpeed',
					'Sw-Host LinkSpeed',
					'Sources',
					'Destinations',
					'NoiseRate',
					'FramesTx',
					'FramesRx',
					'PacketsTx',
					'PacketsRx',
					'avgPSNR'	];
	try:
		with open(OUTPUT_DIR + os.path.sep + 'REPORT.csv', 'rb') as f:
			pass;
	except IOError:
		with open(OUTPUT_DIR + os.path.sep + 'REPORT.csv', 'wb') as f:
			writer = csv.DictWriter(f, fieldnames = fieldnames);
			writer.writeheader();
			pass;
	with open(OUTPUT_DIR + os.path.sep + 'REPORT.csv', 'a+b') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames);
		
		#Create Field Value List
		fieldvalue_list = []
		fieldvalue_list.append([V_NAME + '_v' + str(version)]);
		fieldvalue_list.append([TOPOlOGY_LIST[TOPOLOGY_TYPE - 1]]); # Vertical Format 'Topology'
		fieldvalue_list.append([len(switch_list)]); # Vertical Format 'Switches#'
		fieldvalue_list.append([len(host_list)]); # Vertical Format 'Hosts#'
		fieldvalue_list.append([SWITCH_LINK_SPEED]); # Vertical Format 'Switch-Switch Link Speed'
		fieldvalue_list.append([HOST_LINK_SPEED]); # Vertical Format 'Switch-Host Link Speed'
		fieldvalue_list.append([source_host.name]); # Vertical Format 'Sources'
		fieldvalue_list.append(dest_host_list); # Vertical Format 'Destinations'
		fieldvalue_list.append([noise_rate]); # Vertical Format 'NoiseRate'
		fieldvalue_list.append([frame_count_source]); # Vertical Format 'FramesTx'
		fieldvalue_list.append(frame_count_dest); # Vertical Format 'FramesRx'
		fieldvalue_list.append([packets_sent]); # Vertical Format 'PacketsTx'
		fieldvalue_list.append(packets_recv_list); # Vertical Format 'PacketsRx'
		fieldvalue_list.append(rec_avg_psnr_list); # Vertical Format 'avgPSNR'
		
		# Horizonally Format Rows:
		row_count = 0;
		while True:
			row = {};
			for i in range(len(fieldnames)):
				key = fieldnames[i];
				if row_count < len(fieldvalue_list[i]):
					row[key] = fieldvalue_list[i][row_count];
			if bool(row) == False:
				break;
			writer.writerow(row);
			row_count += 1;
	
	# Clean Residue Processes
	info('\n*** Cleaning Residue Processes . . . ');
	for i in range(len(host_list)):
		ps = host_list[i].cmd('ps | grep -v \"bash\"').split('\n');
		del ps[0];
		for line in ps:
			try:
				pid = int(line.strip().split(' ')[0]);
				host_list[i].cmd('kill -9 ' + str(pid));
			except:
				pass;
	
	# Finished
	info('\n*** Finished.');

# Custom Class for CLI
class CustomCLI(CLI):
	def do_stream(self, _line):
		argv = _line.split();
		if len(argv) > 0 and os.path.isfile(argv[0]) is True:
			arg = os.path.abspath(argv[0]);
		else:
			info('*** Invalid Path!\n');
			return;
		
		# Import Global Vars
		global DESTINATION_COUNT;
		global STREAM_IP;
		global STREAM_PORT;
		global NOISE_PORT;
		global NOISE_DATA_RATE;
		global SAP_PORT;
		global NOISE_PACKET_DELAY;
		
		# Set Streaming Parameters
		while True:
			try:
				MAX_DESTINATION_COUNT = SWITCH_COUNT * HOST_COUNT_PER_SWITCH - 1;
				DESTINATION_COUNT = int(raw_input('Enter number of destinations (>= 1 & <= ' + str(MAX_DESTINATION_COUNT) + '): ') or str(DESTINATION_COUNT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				continue;
			if DESTINATION_COUNT < 1 or DESTINATION_COUNT > MAX_DESTINATION_COUNT:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		while True:
			try:
				STREAM_IP = IP2INT(raw_input('Enter Mutlicast Source IP: ') or STREAM_IP);
			except:
				continue;
			if STREAM_IP == 0:
				info ('*** Error: Invalid Input\n');
				continue;
			IP_RANGE_MIN = IP2INT('224.0.0.1');
			IP_RANGE_MAX = IP2INT('239.255.255.255');
			if STREAM_IP < IP_RANGE_MIN or STREAM_IP > IP_RANGE_MAX:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		while True:
			try:
				STREAM_PORT = int(raw_input('Enter Mutlicast Source Port (>= 1024 & <= 65535): ') or str(STREAM_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				continue;
			if STREAM_PORT < 1024 or STREAM_PORT > 65535:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		while True:
			try:
				NOISE_PORT = int(raw_input('Enter Noise Source Port (>= 1024 & <= 65535): ') or str(NOISE_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				continue;
			if NOISE_PORT < 1024 or NOISE_PORT > 65535:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		
		while True:
			try:
				NOISE_DATA_RATE = int(raw_input('Enter Noise Data Rate (>= 1) (in bps): ') or str(NOISE_DATA_RATE));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				continue;
			if NOISE_DATA_RATE < 1:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		while True:
			try:
				SAP_PORT = int(raw_input('Enter SAP Source Port (>= 1024 & <= 65535): ') or str(SAP_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				continue;
			if SAP_PORT < 1024 or SAP_PORT > 65535:
				info ('*** Error: Input out of range\n');
				continue;
			break;
		NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);
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
