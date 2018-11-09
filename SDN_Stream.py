#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

"""
	Opens process
"""
def mnPopen(host, cmd, fileOut = '/dev/null', shell = True, mnexec = True, executable = '/bin/bash', argv = ['-c']):
	ret = [None, None];
	try:
		gMutex['SUBPROCESS'].acquire();
		
		# Open file
		try:
			with open(fileOut, 'r') as fOut:
				pass;
		except IOError:
			with open(fileOut, 'w') as fOut:
				pass;
		fOut = open(fileOut, 'r+');

		# Prepare Command
		if shell:
			if executable:
				executable = executable + ' ' + ' '.join(pipes.quote(s) for s in argv);
			else:
				executable = str();
			if isinstance(cmd, basestring):
				if mnexec:
					cmd = 'mnexec -a ' + str(host.pid) + ' ' + executable + ' ' + pipes.quote(cmd);
				else:
					cmd = executable + ' ' + pipes.quote(cmd);
			else:
				if mnexec:
					cmd = 'mnexec -a ' + str(host.pid) + ' ' + executable + ' ' + (' '.join(pipes.quote(s) for s in cmd));
				else:
					cmd = executable + ' ' + (' '.join(pipes.quote(s) for s in cmd));
		else:
			if executable:
				executable = [executable] + argv;
			else:
				executable = list();
			if isinstance(cmd, basestring):
				if mnexec:
					cmd = ['mnexec', '-a', str(host.pid)] + executable + shlex.split(cmd);
				else:
					cmd = executable + shlex.split(cmd);
			else:
				if mnexec:
					cmd = ['mnexec', '-a', str(host.pid)] + executable + [' '.join(pipes.quote(s) for s in cmd)];
				else:
					cmd = executable + [' '.join(pipes.quote(s) for s in cmd)];

		ret = host._popen(cmd, stdout = fOut, stderr = fOut, shell = shell, preexec_fn = os.setsid, executable = None), fOut;
	finally:
		time.sleep(0.1);
		gMutex['SUBPROCESS'].release();

	return ret;

"""
	Executes command 
"""
def mnPexec(host, cmd, shell = True, mnexec = True, executable = '/bin/bash', argv = ['-c']):
	proc = None;
	try:
		gMutex['SUBPROCESS'].acquire();

		# Prepare Command
		if shell:
			if executable:
				executable = executable + ' ' + ' '.join(pipes.quote(s) for s in argv);
			else:
				executable = str();
			if isinstance(cmd, basestring):
				if mnexec:
					cmd = 'mnexec -a ' + str(host.pid) + ' ' + executable + ' ' + pipes.quote(cmd);
				else:
					cmd = executable + ' ' + pipes.quote(cmd);
			else:
				if mnexec:
					cmd = 'mnexec -a ' + str(host.pid) + ' ' + executable + ' ' + (' '.join(pipes.quote(s) for s in cmd));
				else:
					cmd = executable + ' ' + (' '.join(pipes.quote(s) for s in cmd));
		else:
			if executable:
				executable = [executable] + argv;
			else:
				executable = list();
			if isinstance(cmd, basestring):
				if mnexec:
					cmd = ['mnexec', '-a', str(host.pid)] + executable + shlex.split(cmd);
				else:
					cmd = executable + shlex.split(cmd);
			else:
				if mnexec:
					cmd = ['mnexec', '-a', str(host.pid)] + executable + [' '.join(pipes.quote(s) for s in cmd)];
				else:
					cmd = executable + [' '.join(pipes.quote(s) for s in cmd)];

		proc = host._popen(cmd, stdout = PIPE, stderr = PIPE, shell = shell, preexec_fn = os.setsid, executable = None);
	finally:
		time.sleep(0.1);
		gMutex['SUBPROCESS'].release();

	# Wait for output
	ret = list(proc.communicate());
	ret.append(proc.wait());
	
	return ret;

def mnPkill(proc, sig = signal.SIGTERM):
	ret = None;
	try:
		gMutex['SUBPROCESS'].acquire();
		os.killpg(os.getpgid(proc.pid), sig);
		ret = proc.wait();
	finally:
		time.sleep(0.1);
		gMutex['SUBPROCESS'].release();
	return ret;

def STREAM(	CASE_ID,
			CLUSTER_ID,
			VIDEO,
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
	try:
		gMutex['STREAM_INIT'].acquire();
		info('\n******************** \n');
		info('*** CLUSTER #' + str(CLUSTER_ID) + ' Host Configuration: \n');
		info('*** \n');

		# Prepare Host Pool
		HOST_POOL = set([x for x in gMain['host_list']]);
		assert(len(HOST_POOL) >= 2);

		# Select Source Host
		source_host = random.choice(gMain['host_list']);
		HOST_POOL.remove(source_host);
		info('*** Source Host: ' + source_host.name + ' (' + source_host.IP(intf = source_host.defaultIntf()) + ')\n');
		info('*** \n');
		
		# Select Destination Hosts
		destination_count = int(DESTINATION_RATIO * len(gMain['host_list']));
		if destination_count < 1:
			destination_count = 1;
		elif destination_count > len(HOST_POOL):
			destination_count = len(HOST_POOL);
		dest_host_list = random.sample(HOST_POOL, destination_count);
		HOST_POOL -= set(dest_host_list);
		info('*** Destination Hosts: \n');
		for host in dest_host_list:
			info('*** ' + host.name + ' (' + host.IP(intf = host.defaultIntf()) + ')\n');
		info('*** \n');

		# Select Noise Hosts
		noise_count = 0;
		noise_host_list = [];
		if NOISE_DATA_RATE > 0:
			if len(HOST_POOL):
				noise_count = int(NOISE_RATIO * len(gMain['host_list']));
				if noise_count < 1:
					noise_count = 1;
				elif noise_count > len(HOST_POOL):
					noise_count = len(HOST_POOL);
				noise_host_list = random.sample(HOST_POOL, noise_count);
				HOST_POOL -= set(noise_host_list);
				info('*** Noise Hosts: \n');
				for host in noise_host_list:
					info('*** ' + host.name + ' (' + host.IP(intf = host.defaultIntf()) + ')\n');
		info('********************\n');

		# Prepare Stream Output Directory
		info('\n[Cluster #' + str(CLUSTER_ID) + '] Preparing Stream Output Directories . . . ');
		start_time = time.time();
		global BASE_DIR;
		EXPORTS_DIR = BASE_DIR + os.path.sep + 'exports';
		assert(os.path.exists(EXPORTS_DIR));
		OUTPUT_DIR = BASE_DIR + os.path.sep + 'output';
		makedirs_s(OUTPUT_DIR);
		CASE_DIR = OUTPUT_DIR + os.path.sep + 'CASE_' + str(CASE_ID);
		makedirs_s(CASE_DIR);
		SOURCE_FILENAME = os.path.split(VIDEO)[1];
		_SOURCE_SPLIT = os.path.splitext(SOURCE_FILENAME);
		V_NAME = _SOURCE_SPLIT[0];
		V_EXT = _SOURCE_SPLIT[1];
		V_VERSION = 1;
		STREAM_DESTDIR = CASE_DIR + os.path.sep + V_NAME;
		while os.path.exists(STREAM_DESTDIR + '_v' + str(V_VERSION)) is True:
			V_VERSION = V_VERSION + 1;
		STREAM_DESTDIR = STREAM_DESTDIR + '_v' + str(V_VERSION);
		makedirs_s(STREAM_DESTDIR);
		STREAM_ID = V_NAME + '_v' + str(V_VERSION)
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
	finally:
		gMutex['STREAM_INIT'].release();

	# Draw Frame# Source Video
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Drawing Frames . . . ');
	[_proc, _f] = mnPopen(host = source_host,
						cmd = 'ffmpeg -i \'' + VIDEO + '\' '
						'-vf \'drawtext=fontfile=Arial.ttf: text=%{n}: x=0: y=0: fontcolor=white: box=1: boxcolor=0x00000099\' '
						'-y \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\'',
						fileOut = LOGS_DIR + os.path.sep + 'ffmpeg_drawtext' + '.log',
						mnexec = not gDockerConfig['ENABLE']);
	_proc.wait();
	_f.flush();
	_f.close();

	# Calculate Source Frame Count
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Calculating Source Frame Count . . . ');
	try:
		frame_count_source = long(mnPexec(	host = source_host,
											cmd = 'ffprobe -v error -count_frames -select_streams v:0 -show_entries '
											'stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 '
											'-i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\'',
											mnexec = not gDockerConfig['ENABLE'])[0].split('\n', 1)[0]);
	except ValueError:
		info('\n[Cluster #' + str(CLUSTER_ID) + '] Error: Reading Source Frames Failed! ');
		return;

	# Generate SDP
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Generating SDP . . . ');
	[_proc, _f] = mnPopen(host = source_host,
						cmd = 'ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
						'-c copy -sdp_file \'' + SDP_DIR + os.path.sep + V_NAME + '_source.sdp\' -t 0 '
						'-f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\'',
						fileOut = LOGS_DIR + os.path.sep + 'sdp.log',
						mnexec = not gDockerConfig['ENABLE']);
	_proc.wait();
	_f.flush();
	_f.close();

	# Start SAP Server
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Starting SAP Server . . . ');
	[_proc, _f] = mnPopen(host = source_host,
						cmd = 'cd \'' + EXPORTS_DIR + '\' && '
						'nice -n -20 python SAP_server.py '
						'\'' + source_host.IP(intf = source_host.defaultIntf()) + '\' '
						'\'' + str(SAP_PORT) + '\' '
						'\'' + SDP_DIR + os.path.sep + V_NAME + '_source.sdp\'',
						fileOut = LOGS_DIR + os.path.sep + 'SAP_server.log',
						mnexec = not gDockerConfig['ENABLE']);

	# Wait 15 Seconds for Topology to update
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Waiting 15 Seconds for Topology to update . . . ');
	time.sleep(15);

	# Start SAP Clients
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Starting SAP Clients . . . ');
	sap_client_command_args_init = 	'cd \'' + EXPORTS_DIR + '\' && nice -n -20 python SAP_client.py ';
	sap_client_process_list = [];
	for host in dest_host_list:
		sap_client_command_args_end = (	'\'' + source_host.IP(intf = source_host.defaultIntf()) + '\' '
										'\'' + str(SAP_PORT) + '\' '
										'\'' + SDP_DIR + os.path.sep + V_NAME + '_destination_' + host.name + '.sdp\'');
		sap_client_process_list.append(mnPopen(	host = host,
												cmd = sap_client_command_args_init + sap_client_command_args_end,
												fileOut = LOGS_DIR + os.path.sep + 'SAP_client_' + host.name + '.log',
												mnexec = not gDockerConfig['ENABLE']));
	for sap_client_process in sap_client_process_list:
		sap_client_process[0].wait();
		sap_client_process[1].flush();
		sap_client_process[1].close();
	info('\n[Cluster #' + str(CLUSTER_ID) + '] SAP Completed! ');
	duration = time.time() - start_time;
	mnPkill(_proc);
	_f.flush();
	_f.close();

	# Initialize Source Packet Capture
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Initializing Source Packet Capture . . . ');
	srcPcapProcess = [None, None];
	[srcPcapProcess[0], srcPcapProcess[1]] = mnPopen(	host = source_host,
											cmd = 'touch \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' && '
											'tshark -i \'' + source_host.defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\'',
											fileOut = LOGS_DIR + os.path.sep + 'tshark_source' + '.log',
											mnexec = not gDockerConfig['ENABLE']);

	# Initialize Destination Packet Capture
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Initializing Destination Packet Capture . . . ');
	dstPcapProcessList = [];
	for host in dest_host_list:
		dstPcapProcessList.append(mnPopen(	host = host,
											cmd = 'touch \'' + PCAP_DIR + os.path.sep + 'destination_host_' + host.name + '.pcap\' && '
											'tshark -i \'' + host.defaultIntf().name + '\' -f \'host ' + INT2IP(STREAM_IP) + ' and port ' + str(STREAM_PORT) + '\' -w \'' + PCAP_DIR + os.path.sep + 'destination_host_' + host.name + '.pcap\'',
											fileOut = LOGS_DIR + os.path.sep + 'tshark_destination_' + host.name + '.log',
											mnexec = not gDockerConfig['ENABLE']));

	# Start Noise
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Starting Noise . . . ');
	# noise_host_list = [];
	# for i in range(1, gMain['host_count']):
	# 	if gMain['host_list'][i] not in dest_host_list:
	# 		noise_host_list.append(gMain['host_list'][i]);
	noiseProcessList = [];
	if NOISE_TYPE == 1:
		for host in noise_host_list:
			noiseProcessList.append(mnPopen(	host = host,
											cmd = 'cd \'' + EXPORTS_DIR + '\' && '
											'python \'Noise_UDP.py\' \'1\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\'',
											fileOut = LOGS_DIR + os.path.sep + 'noise_udp_' + host.name + '.log',
											mnexec = not gDockerConfig['ENABLE']));
	elif NOISE_TYPE == 2:
		_noise_host_offset = noise_count / 2;
		for i in range(0, _noise_host_offset):
			j = _noise_host_offset + i;
			noiseProcessList.append(mnPopen(	host = noise_host_list[i],
											cmd = 'cd \'' + EXPORTS_DIR + '\' && '
											'python \'Noise_UDP.py\' \'2\' \'' + noise_host_list[j].IP(intf = noise_host_list[j].defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\'',
											fileOut = LOGS_DIR + os.path.sep + 'noise_udp_' + noise_host_list[i].name + '.log',
											mnexec = not gDockerConfig['ENABLE']));
			noiseProcessList.append(mnPopen(	host = noise_host_list[j],
											cmd = 'cd \'' + EXPORTS_DIR + '\' && '
											'python \'Noise_UDP.py\' \'2\' \'' + noise_host_list[i].IP(intf = noise_host_list[i].defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\'',
											fileOut = LOGS_DIR + os.path.sep + 'noise_udp_' + noise_host_list[j].name + '.log',
											mnexec = not gDockerConfig['ENABLE']));
		# When Noise Count is Odd (1 Noise Host or Last Noise Host)
		if (noise_count % 2):
			noiseProcessList.append(mnPopen(	host = noise_host_list[-1],
											cmd = 'cd \'' + EXPORTS_DIR + '\' && '
											'python \'Noise_UDP.py\' \'2\' \'' + source_host.IP(intf = source_host.defaultIntf()) + '\' \'' + str(NOISE_PORT) + '\' \'' + str(gPacketConfig['NOISE_PACKET_PAYLOAD_SIZE']) + '\' \'' + str(NOISE_PACKET_DELAY) + '\'',
											fileOut = LOGS_DIR + os.path.sep + 'noise_udp_' + noise_host_list[-1].name + '.log',
											mnexec = not gDockerConfig['ENABLE']));

	# Start Recording
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Starting Recorders . . . ');
	record_args_init = 'nice -n -20 ffmpeg -protocol_whitelist file,udp,rtcp,rtp ';
	_STREAM_STARTED = False;
	_STREAM_COMPLETED = False;
	def _record(_dest_host, _record_args):
		_last = time.time();
		_count = 0;
		while _STREAM_COMPLETED == False and time.time() - _last < 30.0 and _count < 5:
			if _count > 0:
				warn('\n*** WARNING: Recording Failed to Start for \'' + _dest_host.name + '\'. Retry #' + str(_count) + ' . . .');
			_last = time.time();
			[_proc, _f] = mnPopen(host = _dest_host,
								cmd = _record_args,
								fileOut = LOGS_DIR + os.path.sep + 'recorder_' + host.name + '.log',
								mnexec = not gDockerConfig['ENABLE']);
			_proc.wait();
			_f.flush();
			_f.close();
			if _STREAM_STARTED == True:
				_count += 1;
	thread_record_list = [];
	for host in dest_host_list:
		record_args_end =(	'-i \'' + SDP_DIR + os.path.sep + V_NAME + '_destination_' + host.name + '.sdp\' -c copy -y '
							'\'' + REC_DIR + os.path.sep + 'recording_' + host.name + '.ts\'');
		t = threading.Thread(target=_record, args=(host, record_args_init + record_args_end));
		t.start();
		thread_record_list.append(t);

	# Wait 5 Seconds for Recorder to settle
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Waiting 5 Seconds for Recorders to settle . . . ');
	time.sleep(5);

	# Start Streaming
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Preparing Streamers . . . ');
	stream_args =(	'nice -n -20 ffmpeg -re -i \'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\' '
					'-c copy -f rtp -y \'rtp://@' + INT2IP(STREAM_IP) + ':' + str(STREAM_PORT) + '\'');
	[_proc, _f] = mnPopen(host = source_host,
						cmd = stream_args,
						fileOut = LOGS_DIR + os.path.sep + 'streamer.log',
						mnexec = not gDockerConfig['ENABLE']);
	_STREAM_STARTED = True;
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Streaming Started!');
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Waiting for Stream Completion . . . ');
	_proc.wait();
	_f.flush();
	_f.close();
	_STREAM_COMPLETED = True;
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Streaming Completed!');
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Waiting for Record Completion . . . ');
	for thread_record in thread_record_list:
		thread_record.join();
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Recording Completed!');

	# Clean Residue Processes
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Cleaning Residual Processes . . . ');
	# def _clean_residual_processes(_host):
	# 	ps = _host.cmd('ps | grep -v \"bash\"').split('\n');
	# 	del ps[0];
	# 	for line in ps:
	# 		try:
	# 			pid = int(line.strip().split(' ')[0]);
	# 			_host.cmd('kill -9 ' + str(pid));
	# 		except:
	# 			pass;
	# for host in noise_host_list:
	# 	_clean_residual_processes(host);
	# for host in dest_host_list:
	# 	_clean_residual_processes(host);
	# _clean_residual_processes(source_host);
	mnPkill(srcPcapProcess[0]);
	srcPcapProcess[1].flush();
	srcPcapProcess[1].close();
	for dstPcapProcess in dstPcapProcessList:
		mnPkill(dstPcapProcess[0]);
		dstPcapProcess[0].wait();
		dstPcapProcess[1].flush();
		dstPcapProcess[1].close();
	for noiseProcess in noiseProcessList:
		mnPkill(noiseProcess[0]);
		noiseProcess[1].flush();
		noiseProcess[1].close();
	
	# Calculate Received Frame Count
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Calculating Received Frame Counts . . . ');
	frame_count_dest_list = [];
	for host in dest_host_list:
		frame_count_dest = 0;
		try:
			frame_count_dest = long(mnPexec(host = source_host,
											cmd = 	'ffprobe -v error -count_frames -select_streams v:0 -show_entries '
													'stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 '
													'-i \'' + REC_DIR + os.path.sep + 'recording_' + host.name + '.ts\'',
											mnexec = not gDockerConfig['ENABLE'])[0].split('\n', 1)[0]);
		except ValueError:
			pass;
		frame_count_dest_list.append(frame_count_dest);

	# Process PSNR for each Recording
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Processing PSNR Results . . . ');
	rec_avg_mse_list = [];
	rec_avg_psnr_list = [];
	rec_avg_mse_mean = 0.0;
	rec_avg_psnr_mean = 0.0;
	for host in dest_host_list:
		[_proc, _f] = mnPopen(host = host,
							cmd = 'ffmpeg -i \'' + REC_DIR + os.path.sep + 'recording_' + host.name + '.ts\' '
							'-vf \"movie=\'' + STREAM_DESTDIR + os.path.sep + 'mod_' + SOURCE_FILENAME + '\', psnr=stats_file=\'' + PSNR_DIR + os.path.sep + 'rec_' + host.name + '_psnr.txt\'\" '
							'-f rawvideo -y /dev/null',
							fileOut = LOGS_DIR + os.path.sep + 'rec_' + host.name + '_psnr' + '.log',
							mnexec = not gDockerConfig['ENABLE']);
		_proc.wait();
		_f.flush();
		_f.close();
		try:
			with open(PSNR_DIR + os.path.sep + 'rec_' + host.name + '_psnr.txt', 'r') as f:
				pass;
		except IOError:
			with open(PSNR_DIR + os.path.sep + 'rec_' + host.name + '_psnr.txt', 'w') as f:
				pass;
		with open(PSNR_DIR + os.path.sep + 'rec_' + host.name + '_psnr.txt', 'r+') as f:
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
	rec_avg_mse_mean = get_mean(rec_avg_mse_list);
	try:
		rec_avg_psnr_mean = 10 * math.log10(255 * 255 / rec_avg_mse_mean);
	except:
		rec_avg_psnr_mean = float('inf'); # Make sure to not use this value for calculation anywhere!
		
	# Process Packets Sent/Received
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Processing PCAP Results . . . ');
	packets_sent = -1;
	try:
		packets_sent_response = mnPexec(	host = source_host,
											cmd = 'tshark -r \'' + PCAP_DIR + os.path.sep + 'source_host.pcap\' '
											'-q -z io,phs | sed -n \'7,7p\' | cut -d \' \' -f 40 | cut -d \':\' -f 2',
											mnexec = not gDockerConfig['ENABLE'])[0].split('\n');
		for x in packets_sent_response:
			try:
				packets_sent = int(x);
			except ValueError:
				pass;
			else:
				break;
	except:
		pass;
	packets_recv_list = [];
	for host in dest_host_list:
		packets_recv = -1;
		try:
			packets_recv_response = mnPexec(	host = host,
												cmd = 'tshark -r \'' + PCAP_DIR + os.path.sep + 'destination_host_' + host.name + '.pcap\' '
												'-q -z io,phs | sed -n \'7,7p\' | cut -d \' \' -f 40 | cut -d \':\' -f 2',
												mnexec = not gDockerConfig['ENABLE'])[0].split('\n');
			for x in packets_recv_response:
				try:
					packets_recv = int(x);
				except ValueError:
					pass;
				else:
					break;
		except:
			pass;
		packets_recv_list.append(packets_recv);

	# Retrieve Noise Rate (Not Required - Only for Testing)
	# info('\n*** Retrieving Noise Rate . . . ');
	# try:
	# 	with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'r') as f:
	# 		pass;
	# except IOError:
	# 	with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'w') as f:
	# 		pass;
	# with open(LOGS_DIR + os.path.sep + 'noise_udp' + '.log', 'r+') as f: 
	# 	content = f.readlines();
	# 	noise_rate = 0.0;
	# 	for line in content:
	# 		text = line.split(' ');
	# 		if text[0] == 'DATA_RATE':
	# 			try:
	# 				noise_rate = float(text[1]);
	# 			except ValueError:
	# 				noise_rate = -1;
	# 			break;
	
	# Retrieve Path Metrics
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Retrieving Path Metrics . . . ');
	multicast_path_hopcount = '-';
	multicast_path_latency = '-';
	multicast_path_cost = '-';
	srcSwId = '';
	for i in range(gMain['switch_count']):
		for j in range(len(gMain['switch_host_list'][i])):
			if source_host == gMain['switch_host_list'][i][j]:
				_dpid = gMain['switch_list'][i].dpid;
				srcSwId = ':'.join(a+b for a,b in zip(_dpid[::2], _dpid[1::2]));
				break;
		if srcSwId:
			break;
	try:
		_url = "http://127.0.0.1:8080//wm/sessionmanager/pathStats";
		_url = _url + "?" + "srcSwId=" + str(srcSwId);
		_url = _url + "&" + "dstIPAddress=" + str(INT2IP(STREAM_IP));
		_url = _url + "&" + "dstTransportPort=" + str(STREAM_PORT);
		_request = urllib2.Request(_url);
		_response = urllib2.build_opener(urllib2.ProxyHandler({})).open(_request).read(); # Bypass Proxy
		_data = json.loads(_response);
		multicast_path_hopcount = _data['HopCount'];
		multicast_path_latency = _data['Latency'];
		multicast_path_cost = _data['Cost'];
	except urllib2.HTTPError as e:
		if e.code == 404:
			warn('\nWARNING: Path Metrics not Found')
		else:
			warn('\nERROR: ' + str(e));
	except Exception as e:
		warn('\nERROR: ' + str(e));
	
	# Create Report
	try:
		gMutex['STREAM_END'].acquire();
		info('\n[Cluster #' + str(CLUSTER_ID) + '] Generating Report . . . ');
		fieldnames = [	'CASE_ID',
						'CLUSTER_ID',
						'STREAM_ID',
						'Config_TOPOLOGY_TYPE',
						'Config_SWITCH_COUNT',
						'Config_HOST_COUNT_PER_SWITCH',
						'Config_USE_STP',
						'Config_SWITCH_LINK_SPEED',
						'Config_HOST_LINK_SPEED',
						'Config_RANDOM_SWITCH_GLOBAL_MAX_LINKS',
						'Config_RANDOM_TOTAL_HOST_COUNT',
						'StreamConfig_VIDEO',
						'StreamConfig_DESTINATION_RATIO',
						'StreamConfig_STREAM_IP',
						'StreamConfig_STREAM_PORT',
						'StreamConfig_NOISE_TYPE',
						'StreamConfig_NOISE_RATIO',
						'StreamConfig_NOISE_PORT',
						'StreamConfig_NOISE_DATA_RATE',
						'StreamConfig_NOISE_PACKET_DELAY',
						'StreamConfig_SAP_PORT',
						'Duration',
						'TotalSwitchCount',
						'TotalHostCount',
						'NoiseHosts',
						'SourceHosts',
						'DestinationHosts',
						'MulticastPath_HopCount',
						'MulticastPath_Latency',
						'MulticastPath_Cost',
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
			fieldvalue.append(CASE_ID); # 'CASE_ID'
			fieldvalue.append(CLUSTER_ID); # 'CLUSTER_ID'
			fieldvalue.append(STREAM_ID); # 'STREAM_ID'
			fieldvalue.append(gConfig['TOPOLOGY_TYPE']); # 'Config_TOPOLOGY_TYPE'
			fieldvalue.append(gConfig['SWITCH_COUNT']); # 'Config_SWITCH_COUNT'
			fieldvalue.append(gConfig['HOST_COUNT_PER_SWITCH']); # 'Config_HOST_COUNT_PER_SWITCH'
			fieldvalue.append(gConfig['USE_STP']); # 'Config_USE_STP'
			fieldvalue.append(gConfig['SWITCH_LINK_SPEED']); # 'Config_SWITCH_LINK_SPEED'
			fieldvalue.append(gConfig['HOST_LINK_SPEED']); # 'Config_HOST_LINK_SPEED'
			fieldvalue.append(gConfig['RANDOM_SWITCH_GLOBAL_MAX_LINKS'] if (gConfig['TOPOLOGY_TYPE'] == 5) else -1); # 'Config_RANDOM_SWITCH_GLOBAL_MAX_LINKS'
			fieldvalue.append(gConfig['RANDOM_TOTAL_HOST_COUNT'] if (gConfig['TOPOLOGY_TYPE'] == 5) else -1); # 'Config_RANDOM_TOTAL_HOST_COUNT'
			fieldvalue.append(VIDEO); # 'StreamConfig_VIDEO'
			fieldvalue.append(DESTINATION_RATIO); # 'StreamConfig_DESTINATION_RATIO'
			fieldvalue.append(INT2IP(STREAM_IP)); # 'StreamConfig_STREAM_IP'
			fieldvalue.append(STREAM_PORT); # 'StreamConfig_STREAM_PORT'
			fieldvalue.append(NOISE_TYPE); # 'StreamConfig_NOISE_TYPE'
			fieldvalue.append(NOISE_RATIO); # 'StreamConfig_NOISE_RATIO'
			fieldvalue.append(NOISE_PORT); # 'StreamConfig_NOISE_PORT'
			fieldvalue.append(NOISE_DATA_RATE); # 'StreamConfig_NOISE_DATA_RATE'
			fieldvalue.append(NOISE_PACKET_DELAY); # 'StreamConfig_NOISE_PACKET_DELAY'
			fieldvalue.append(SAP_PORT); # 'StreamConfig_SAP_PORT'
			fieldvalue.append(duration); # 'Duration'
			fieldvalue.append(len(gMain['switch_list'])); # 'TotalSwitchCount'
			fieldvalue.append(len(gMain['host_list'])); # 'TotalHostCount'
			fieldvalue.append(len(noise_host_list)); # 'NoiseHosts'
			fieldvalue.append(1); # 'SourceHosts'
			fieldvalue.append(len(dest_host_list)); # 'DestinationHosts'
			fieldvalue.append(multicast_path_hopcount); # 'MulticastPath_HopCount'
			fieldvalue.append(multicast_path_latency); # 'MulticastPath_Latency'
			fieldvalue.append(multicast_path_cost); # 'MulticastPath_Cost'
			fieldvalue.append(frame_count_source); # 'FramesTx'
			fieldvalue.append(get_mean(frame_count_dest_list)); # 'FramesRx'
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
			fieldvalue_list.append([CASE_ID]); # Vertical Format 'CASE_ID'
			fieldvalue_list.append([CLUSTER_ID]); # Vertical Format 'CLUSTER_ID'
			fieldvalue_list.append([STREAM_ID]); # Vertical Format 'STREAM_ID'
			fieldvalue_list.append([gConfig['TOPOLOGY_TYPE']]); # Vertical Format 'Config_TOPOLOGY_TYPE'
			fieldvalue_list.append([gConfig['SWITCH_COUNT']]); # Vertical Format 'Config_SWITCH_COUNT'
			fieldvalue_list.append([gConfig['HOST_COUNT_PER_SWITCH']]); # Vertical Format 'Config_HOST_COUNT_PER_SWITCH'
			fieldvalue_list.append([gConfig['USE_STP']]); # Vertical Format 'Config_USE_STP'
			fieldvalue_list.append([gConfig['SWITCH_LINK_SPEED']]); # Vertical Format 'Config_SWITCH_LINK_SPEED'
			fieldvalue_list.append([gConfig['HOST_LINK_SPEED']]); # Vertical Format 'Config_HOST_LINK_SPEED'
			fieldvalue_list.append([gConfig['RANDOM_SWITCH_GLOBAL_MAX_LINKS'] if (gConfig['TOPOLOGY_TYPE'] == 5) else -1]); # Vertical Format 'Config_RANDOM_SWITCH_GLOBAL_MAX_LINKS'
			fieldvalue_list.append([gConfig['RANDOM_TOTAL_HOST_COUNT'] if (gConfig['TOPOLOGY_TYPE'] == 5) else -1]); # Vertical Format 'Config_RANDOM_TOTAL_HOST_COUNT'
			fieldvalue_list.append([VIDEO]); # Vertical Format 'StreamConfig_VIDEO'
			fieldvalue_list.append([DESTINATION_RATIO]); # Vertical Format 'StreamConfig_DESTINATION_RATIO'
			fieldvalue_list.append([INT2IP(STREAM_IP)]); # Vertical Format 'StreamConfig_STREAM_IP'
			fieldvalue_list.append([STREAM_PORT]); # Vertical Format 'StreamConfig_STREAM_PORT'
			fieldvalue_list.append([NOISE_TYPE]); # Vertical Format 'StreamConfig_NOISE_TYPE'
			fieldvalue_list.append([NOISE_RATIO]); # Vertical Format 'StreamConfig_NOISE_RATIO'
			fieldvalue_list.append([NOISE_PORT]); # Vertical Format 'StreamConfig_NOISE_PORT'
			fieldvalue_list.append([NOISE_DATA_RATE]); # Vertical Format 'StreamConfig_NOISE_DATA_RATE'
			fieldvalue_list.append([NOISE_PACKET_DELAY]); # Vertical Format 'StreamConfig_NOISE_PACKET_DELAY'
			fieldvalue_list.append([SAP_PORT]); # Vertical Format 'StreamConfig_SAP_PORT'
			fieldvalue_list.append([duration]); # Vertical Format 'Duration'
			fieldvalue_list.append([len(gMain['switch_list'])]); # Vertical Format 'TotalSwitchCount'
			fieldvalue_list.append([len(gMain['host_list'])]); # Vertical Format 'TotalHostCount'
			fieldvalue_list.append(noise_host_list); # Vertical Format 'NoiseHosts'
			fieldvalue_list.append([source_host.name]); # Vertical Format 'SourceHosts'
			fieldvalue_list.append(dest_host_list); # Vertical Format 'DestinationHosts'
			fieldvalue_list.append([multicast_path_hopcount]); # 'MulticastPath_HopCount'
			fieldvalue_list.append([multicast_path_latency]); # 'MulticastPath_Latency'
			fieldvalue_list.append([multicast_path_cost]); # 'MulticastPath_Cost'
			fieldvalue_list.append([frame_count_source]); # Vertical Format 'FramesTx'
			fieldvalue_list.append(frame_count_dest_list); # Vertical Format 'FramesRx'
			fieldvalue_list.append([packets_sent]); # Vertical Format 'PacketsTx'
			fieldvalue_list.append(packets_recv_list); # Vertical Format 'PacketsRx'
			fieldvalue_list.append(rec_avg_psnr_list); # Vertical Format 'avgPSNR'
			
			# Horizonally Format Rows:
			row_count = 0;
			while True:
				row = {};
				is_valid = False;
				for i in range(len(fieldnames)):
					key = fieldnames[i];
					if row_count < len(fieldvalue_list[i]):
						row[key] = fieldvalue_list[i][row_count];
						is_valid = True;	# row is valid only if at least 1 column is different from previous row.
					# elif len(fieldvalue_list[i]):
						# row[key] = fieldvalue_list[i][-1];	# print last element if the list corresponding to the given column is exhausted.
					else:
						row[key] = '-';	# list corresponding to the given column is empty.
				if not row or not is_valid:
					break;
				# Write to file
				writer.writerow(row);
				row_count += 1;
	finally:
		gMutex['STREAM_END'].release();

	# Finished
	info('\n[Cluster #' + str(CLUSTER_ID) + '] Finished.\n');
