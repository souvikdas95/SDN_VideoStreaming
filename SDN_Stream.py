#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

def STREAM(	VIDEO,
			DESTINATION_RATIO,
			STREAM_IP,
			STREAM_PORT,
			NOISE_RATIO,
			NOISE_TYPE,
			NOISE_PORT,
			NOISE_DATA_RATE,
			NOISE_PACKET_DELAY,
			SAP_PORT):
	# Delay & Print
	time.sleep(0.1);
	sys.stdout.flush();
	info('\n');
	
	# Print Required Source Destination Noise Hosts Information
	info('\n********************\n');
	source_host = gMain['host_list'][0];
	info('*** Source Host: ' + source_host.name + ' (' + source_host.IP(intf = source_host.defaultIntf()) + ')\n');
	destination_count = int(DESTINATION_RATIO * gMain['host_count']);
	if destination_count < 1:
		destination_count = 1;
	elif destination_count > gMain['host_count'] - 1:
		destination_count = gMain['host_count'] - 1;
	dest_host_list = random.sample(gMain['host_list'][1::], destination_count);
	info('*** Destination Hosts: \n');
	for i in range(destination_count):
		info('*** ' + dest_host_list[i].name + ' (' + dest_host_list[i].IP(intf = dest_host_list[i].defaultIntf()) + ')\n');
	noise_count = int(NOISE_RATIO * gMain['host_count']);
	if noise_count < 1 and destination_count + 1 <= gMain['host_count'] - 1:
		noise_count = 1;
	elif noise_count > gMain['host_count'] - 1 - destination_count:
		noise_count = gMain['host_count'] - 1 - destination_count;
	noise_host_list = random.sample(set(gMain['host_list'][1::]) - set(dest_host_list), noise_count);
	info('*** Noise Hosts: \n');
	for i in range(noise_count):
		info('*** ' + noise_host_list[i].name + ' (' + noise_host_list[i].IP(intf = noise_host_list[i].defaultIntf()) + ')\n');
	info('********************\n');
	
	# Prepare Stream Output Directory
	info('\n*** Preparing Stream Output Directories . . . ');
	start_time = time.time();
	global BASE_DIR;
	OUTPUT_DIR = BASE_DIR + os.path.sep + 'output';
	makedirs_s(OUTPUT_DIR);
	EXPORTS_DIR = BASE_DIR + os.path.sep + 'exports';
	SOURCE_FILENAME = os.path.split(VIDEO)[1];
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
	source_host.cmd('ffmpeg -i \'' + VIDEO + '\' '
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
	source_host.cmd('cd \'' + EXPORTS_DIR + '\' && '
					'python SAP_server.py '
					'\'' + source_host.IP(intf = source_host.defaultIntf()) + '\' '
					'\'' + str(SAP_PORT) + '\' '
					'\'' + SDP_DIR + os.path.sep + V_NAME + '_source.sdp\' '
					'&> \'' + LOGS_DIR + os.path.sep + 'SAP_server.log\' 2>&1 &');
	sap_client_command_args_init = 	'cd \'' + EXPORTS_DIR + '\' && python SAP_client.py ';
	def _sap_client_command(_dest_host, _sap_client_command_args):
		_dest_host.cmd(_sap_client_command_args);
	thread_sap_client_list = [];
	for i in range(destination_count):
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
	duration = time.time() - start_time;

	# Initialize Source Packet Capture
	info('\n*** Initializing Source Packet Capture . . . ');
	source_host.cmd('touch \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' && '
					'tshark -i \'' + source_host.defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' '
					'&> \'' + LOGS_DIR + os.path.sep + 'tshark_source' + '.log\' 2>&1 &');

	# Initialize Destination Packet Capture
	info('\n*** Initializing Destination Packet Capture . . . ');
	for i in range(destination_count):
		dest_host_list[i].cmd(	'touch \'' + PCAP_DIR + os.path.sep + 'destination_host_' + str(i) + '.pcap\' && '
								'tshark -i \'' + dest_host_list[i].defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'destination_host_' + str(i) + '.pcap\' '
								'&> \'' + LOGS_DIR + os.path.sep + 'tshark_destination_' + str(i) + '.log\' 2>&1 &');

	# Start Noise
	info('\n*** Starting Noise . . . ');
	# noise_host_list = [];
	# for i in range(1, gMain['host_count']):
	# 	if gMain['host_list'][i] not in dest_host_list:
	# 		noise_host_list.append(gMain['host_list'][i]);
	if NOISE_TYPE == 1:
		for i in range(0, noise_count):
			noise_host_list[i].cmd(	'cd \'' + EXPORTS_DIR + '\' && '
									'python \'Noise_UDP.py\' \'1\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
									'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');
	elif NOISE_TYPE == 2:
		_noise_host_offset = noise_count / 2;
		for i in range(0, _noise_host_offset):
			j = _noise_host_offset + i;
			noise_host_list[i].cmd(	'cd \'' + EXPORTS_DIR + '\' && '
									'python \'Noise_UDP.py\' \'2\' \'' + noise_host_list[j].IP(intf = noise_host_list[j].defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
									'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');
			noise_host_list[j].cmd(	'cd \'' + EXPORTS_DIR + '\' && '
									'python \'Noise_UDP.py\' \'2\' \'' + noise_host_list[i].IP(intf = noise_host_list[i].defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
									'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');
		# When Noise Count is Odd (1 Noise Host or Last Noise Host)
		if (noise_count % 2):
			noise_host_list[-1].cmd(	'cd \'' + EXPORTS_DIR + '\' && '
										'python \'Noise_UDP.py\' \'2\' \'' + source_host.IP(intf = source_host.defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\' '
										'&> \'' + LOGS_DIR + os.path.sep + 'noise_udp' + '.log\' 2>&1 &');


	# Wait for 15 Seconds
	info('\n*** Wait 15 Seconds for Network to Settle . . . ');
	time.sleep(15);

	# Prepare Stream Recorders
	info('\n*** Preparing Stream Recorders . . . ');
	record_args_init = 'ffmpeg -protocol_whitelist file,udp,rtcp,rtp ';
	_STREAM_COMPLETED = False;
	def _record(_dest_host, _record_args):
		_last = time.time();
		_count = 0;
		while _STREAM_COMPLETED == False and time.time() - _last < 30.0 and _count < 10:
			if _count > 0:
				warn('\n*** WARNING: Recording Failed to Start for \'' + _dest_host.name + '\'. Retry #' + str(_count) + ' . . .');
			_last = time.time();
			_dest_host.cmd(_record_args);
			_count += 1;
	thread_record_list = [];
	for i in range(destination_count):
		record_args_end =(	'-i \'' + SDP_DIR + os.path.sep + V_NAME + '_destination_' + str(i) + '.sdp\' -c copy -y '
							'\'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
							'>> \'' + LOGS_DIR + os.path.sep + 'recorder_' + str(i) + '.log\' 2>&1');
		t = threading.Thread(target=_record, args=(dest_host_list[i], record_args_init + record_args_end));
		t.start();
		thread_record_list.append(t);
	time.sleep(1);

	# Start Streamer
	stream_args =(	'ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\' '
					'> \'' + LOGS_DIR + os.path.sep + 'streamer.log\' 2>&1');
	source_host.sendCmd(stream_args);
	info('\n*** Streaming Started . . . ');

	# Wait for Stream Completion
	source_host.waitOutput(verbose = False, findPid = False);
	info('\n*** Streaming Completed . . . ');
	_STREAM_COMPLETED = True;
	info('\n*** Waiting for Record Completion . . . ');
	for thread_record in thread_record_list:
		thread_record.join();
	info('\n*** Recording Completed . . . ');

	# Clean Residue Processes
	info('\n*** Cleaning Residue Processes . . . ');
	for i in range(gMain['host_count']):
		ps = gMain['host_list'][i].cmd('ps | grep -v \"bash\"').split('\n');
		del ps[0];
		for line in ps:
			try:
				pid = int(line.strip().split(' ')[0]);
				gMain['host_list'][i].cmd('kill -9 ' + str(pid));
			except:
				pass;

	# Process PSNR for each Recording
	info('\n*** Processing PSNR Results . . . ');
	rec_avg_mse_list = [];
	rec_avg_psnr_list = [];
	rec_avg_mse_mean = 0.0;
	rec_avg_psnr_mean = 0.0;
	frame_count_dest = [];
	for i in range(destination_count):
		dest_host_list[i].cmd(	'ffmpeg -i \'' + REC_DIR + os.path.sep + 'recording_' + str(i) + '.ts\' '
								'-vf \"movie=\'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\', psnr=stats_file=\'' + PSNR_DIR + os.path.sep + 'rec_' + str(i) + '_psnr.txt\'\" '
								'-f rawvideo -y /dev/null '
								'> \'' + LOGS_DIR + os.path.sep + 'rec_' + str(i) + '_psnr' + '.log\' 2>&1');
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
			# Assuming BitDepth is fixed at 8-bit
			if frame_count == 0:
				avg_mseavg = 255 * 255;
			else:
				avg_mseavg = avg_mseavg / frame_count;
				if avg_mseavg > 255 * 255:
					avg_mseavg = 255 * 255;
			try:
				avg_psnr = 10 * math.log10(255 * 255 / avg_mseavg);
			except:
				avg_psnr = float('inf'); # Make sure to not use this value for calculation anywhere!
			rec_avg_mse_list.append(avg_mseavg);
			rec_avg_psnr_list.append(avg_psnr);
			frame_count_dest.append(frame_count);
	rec_avg_mse_mean = get_mean(rec_avg_mse_list);
	try:
		rec_avg_psnr_mean = 10 * math.log10(255 * 255 / rec_avg_mse_mean);
	except:
		rec_avg_psnr_mean = float('inf'); # Make sure to not use this value for calculation anywhere!
		
	# Process Packets Sent/Received
	info('\n*** Processing PCAP Results . . . ');
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
	for i in range(destination_count):
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
					'NoiseType',
					'NoiseRate',
					'Duration',
					'FramesTx',
					'FramesRx',
					'PacketsTx',
					'PacketsRx',
					'avgPSNR'	];

	# Brief Report
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
		fieldvalue = []
		fieldvalue.append(V_NAME + '_v' + str(version));
		fieldvalue.append(gConfig['TOPOLOGY_LIST'][gConfig['TOPOLOGY_TYPE'] - 1]); # 'Topology'
		fieldvalue.append(len(gMain['switch_list'])); # 'Switches#'
		fieldvalue.append(len(gMain['host_list'])); # 'Hosts#'
		fieldvalue.append(gConfig['SWITCH_LINK_SPEED']); # 'Switch-Switch Link Speed'
		fieldvalue.append(gConfig['HOST_LINK_SPEED']); # 'Switch-Host Link Speed'
		fieldvalue.append(source_host.name); # 'Sources'
		fieldvalue.append(len(dest_host_list)); # 'Destinations'
		fieldvalue.append(NOISE_TYPE); # 'NoiseType'
		fieldvalue.append(noise_rate); # 'NoiseRate'
		fieldvalue.append(duration); # 'Duration'
		fieldvalue.append(frame_count_source); # 'FramesTx'
		fieldvalue.append(get_mean(frame_count_dest)); # 'FramesRx'
		fieldvalue.append(packets_sent); # 'PacketsTx'
		fieldvalue.append(get_mean(packets_recv_list)); # 'PacketsRx'
		fieldvalue.append(rec_avg_psnr_mean); # 'avgPSNR'
		
		# Write to file
		row = dict(zip(fieldnames, fieldvalue));
		if row:
			writer.writerow(row);

	# Detailed Report
	try:
		with open(OUTPUT_DIR + os.path.sep + 'REPORT_DETAIL.csv', 'rb') as f:
			pass;
	except IOError:
		with open(OUTPUT_DIR + os.path.sep + 'REPORT_DETAIL.csv', 'wb') as f:
			writer = csv.DictWriter(f, fieldnames = fieldnames);
			writer.writeheader();
			pass;
	with open(OUTPUT_DIR + os.path.sep + 'REPORT_DETAIL.csv', 'a+b') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames);
		
		#Create Field Value List
		fieldvalue_list = []
		fieldvalue_list.append([V_NAME + '_v' + str(version)]);
		fieldvalue_list.append([gConfig['TOPOLOGY_LIST'][gConfig['TOPOLOGY_TYPE'] - 1]]); # Vertical Format 'Topology'
		fieldvalue_list.append([len(gMain['switch_list'])]); # Vertical Format 'Switches#'
		fieldvalue_list.append([len(gMain['host_list'])]); # Vertical Format 'Hosts#'
		fieldvalue_list.append([gConfig['SWITCH_LINK_SPEED']]); # Vertical Format 'Switch-Switch Link Speed'
		fieldvalue_list.append([gConfig['HOST_LINK_SPEED']]); # Vertical Format 'Switch-Host Link Speed'
		fieldvalue_list.append([source_host.name]); # Vertical Format 'Sources'
		fieldvalue_list.append(dest_host_list); # Vertical Format 'Destinations'
		fieldvalue_list.append([NOISE_TYPE]); # Vertical Format 'NoiseType'
		fieldvalue_list.append([noise_rate]); # Vertical Format 'NoiseRate'
		fieldvalue_list.append([duration]); # Vertical Format 'Duration'
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
			if not row:
				break;
			# Write to file
			writer.writerow(row);
			row_count += 1;

	# Finished
	info('\n*** Finished.\n');
