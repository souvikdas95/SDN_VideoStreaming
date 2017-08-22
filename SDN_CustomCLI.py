#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Import STREAM method
from SDN_Stream import STREAM;

# Custom Class for CLI
class CustomCLI(CLI):
	def __init__(self, *args, **kwargs):
		if gArg['argv']:
			info ('*** Initiating Streaming . . .\n');
			self.do_stream(gStreamConfig['SOURCE']);
		CLI.__init__(self, *args, **kwargs);

	def do_stream(self, _line):
		argv = _line.split();
		if len(argv) > 0 and os.path.isfile(argv[0]) is True:
			STREAM_SRC = os.path.abspath(argv[0]);
		else:
			info('*** Error: Invalid Path!\n');
			if gArg['argv']:
				Cleanup.cleanup();
				sys.exit(0);
			return;
		
		# Default Configuration for STREAM
		MTU = gPacketConfig['MTU'];
		DESTINATION_COUNT = gStreamConfig['DESTINATION_COUNT'];
		STREAM_IP = gStreamConfig['STREAM_IP'];
		STREAM_PORT = gStreamConfig['STREAM_PORT'];
		NOISE_TYPE = gStreamConfig['NOISE_TYPE'];
		NOISE_DESTINATION_PORT = gStreamConfig['NOISE_DESTINATION_PORT'];
		NOISE_DATA_RATE = gStreamConfig['NOISE_DATA_RATE'];
		NOISE_PACKET_DELAY = gStreamConfig['NOISE_PACKET_DELAY'];
		SAP_PORT = gStreamConfig['SAP_PORT'];
		
		# Set Streaming Parameters
		while True:
			try:
				MAX_DESTINATION_COUNT = gMain['host_count'] - 1;
				DESTINATION_COUNT = int(get_input('Enter number of destinations (>= 1 & <= ' + str(MAX_DESTINATION_COUNT) + '): ') or str(DESTINATION_COUNT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if DESTINATION_COUNT < 1 or DESTINATION_COUNT > MAX_DESTINATION_COUNT:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				STREAM_IP = IP2INT(get_input('Enter Mutlicast Source IP: ') or INT2IP(STREAM_IP));
			except:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if STREAM_IP == 0:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			IP_RANGE_MIN = IP2INT('224.0.0.1');
			IP_RANGE_MAX = IP2INT('239.255.255.255');
			if STREAM_IP < IP_RANGE_MIN or STREAM_IP > IP_RANGE_MAX:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				STREAM_PORT = int(get_input('Enter Mutlicast Source Port (>= 1024 & <= 65535): ') or str(STREAM_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if STREAM_PORT < 1024 or STREAM_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				NOISE_TYPE = int(get_input('Enter Noise Type (1:Broadcast, 2:Unicast): ') or str(NOISE_TYPE));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if NOISE_TYPE not in range(1, 2 + 1):
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				NOISE_DESTINATION_PORT = int(get_input('Enter Noise Destination Port (>= 1024 & <= 65535): ') or str(NOISE_DESTINATION_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if NOISE_DESTINATION_PORT < 1024 or NOISE_DESTINATION_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				NOISE_DATA_RATE = int(get_input('Enter Noise Data Rate per Host (>= 1) (in bps): ') or str(NOISE_DATA_RATE));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if NOISE_DATA_RATE < 1:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		while True:
			try:
				SAP_PORT = int(get_input('Enter SAP Source Port (>= 1024 & <= 65535): ') or str(SAP_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			if SAP_PORT < 1024 or SAP_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
			break;
		NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);

		# Call STREAM method on Separate Thread
		t = threading.Thread(target = STREAM, args = (
			STREAM_SRC,
			DESTINATION_COUNT,
			STREAM_IP,
			STREAM_PORT,
			NOISE_TYPE,
			NOISE_DESTINATION_PORT,
			NOISE_DATA_RATE,
			NOISE_PACKET_DELAY,
			SAP_PORT));
		t.start();