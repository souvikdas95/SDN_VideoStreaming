#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Import Shlex (For parameter parsing)
import shlex;

# Import STREAM method
from SDN_Stream import STREAM;

# Custom Class for CLI
class CustomCLI(CLI):
	def __init__(self, *args, **kwargs):
		self.cliArg = {
			'argv' : None,
			'cur' : 0,
			'test' : 0,
			'test_file' : None,
		};
		if gArg['argv']:
			self.cliArg['test_file'] = gArg['argv'][-1] or self.cliArg['test_file'];
			try:
				with open(BASE_DIR + os.path.sep + self.cliArg['test_file'], 'rt') as f:
					for _line in f:
						self.cliArg['argv'] = shlex.split(_line);
						self.cliArg['cur'] = 0;
						self.cliArg['test'] += 1;
						self.do_stream();
			except IOError:
				info('*** Error: Couldn\'t open Stream test file: \'' + self.cliArg['test_file'] + '\'!\n');
			Cleanup.cleanup();
			sys.exit(0);
		CLI.__init__(self, *args, **kwargs);

	def _get_input(self, _str):
		if self.cliArg['argv']:
			if self.cliArg['cur'] < len(self.cliArg['argv']):
				_input = self.cliArg['argv'][self.cliArg['cur']];
				self.cliArg['cur'] += 1;
			else:
				_input = '';
		else:
			_input = raw_input(_str);
		return _input;

	def do_stream(self, *args, **kwargs):
		""" Method to initialize Streaming """
		if self.cliArg['argv']:
			info('\n\n****** STREAMING TEST #' + str(self.cliArg['test']) + '\n');

		# Default Configuration for STREAM
		VIDEO = gStreamConfig['VIDEO']
		DESTINATION_RATIO = gStreamConfig['DESTINATION_RATIO'];
		STREAM_IP = gStreamConfig['STREAM_IP'];
		STREAM_PORT = gStreamConfig['STREAM_PORT'];
		NOISE_RATIO = gStreamConfig['NOISE_RATIO'];
		NOISE_TYPE = gStreamConfig['NOISE_TYPE'];
		NOISE_PORT = gStreamConfig['NOISE_PORT'];
		NOISE_DATA_RATE = gStreamConfig['NOISE_DATA_RATE'];
		NOISE_PACKET_DELAY = gStreamConfig['NOISE_PACKET_DELAY'];
		SAP_PORT = gStreamConfig['SAP_PORT'];
		
		# Set Streaming Parameters
		while True:
			try:
				VIDEO = os.path.abspath(self._get_input('Enter Stream Source file path: ') or VIDEO);
			except:
				info ('*** Error: Couldn\'t open Stream Source file\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				DESTINATION_RATIO = float(self._get_input('Enter Destination Ratio: ') or str(DESTINATION_RATIO));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if DESTINATION_RATIO < 0.0 or DESTINATION_RATIO > 1.0:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				STREAM_IP = IP2INT(self._get_input('Enter Mutlicast Source IP: ') or INT2IP(STREAM_IP));
			except:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if STREAM_IP == 0:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			IP_RANGE_MIN = IP2INT('224.0.0.1');
			IP_RANGE_MAX = IP2INT('239.255.255.255');
			if STREAM_IP < IP_RANGE_MIN or STREAM_IP > IP_RANGE_MAX:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				STREAM_PORT = int(self._get_input('Enter Mutlicast Source Port (>= 1024 & <= 65535): ') or str(STREAM_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if STREAM_PORT < 1024 or STREAM_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				NOISE_RATIO = float(self._get_input('Enter Noise Ratio: ') or str(NOISE_RATIO));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if NOISE_RATIO < 0.0 or NOISE_RATIO > 1.0:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				NOISE_TYPE = int(self._get_input('Enter Noise Type (1:Broadcast, 2:Unicast): ') or str(NOISE_TYPE));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if NOISE_TYPE not in range(1, 2 + 1):
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				NOISE_PORT = int(self._get_input('Enter Noise Destination Port (>= 1024 & <= 65535): ') or str(NOISE_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if NOISE_PORT < 1024 or NOISE_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				NOISE_DATA_RATE = int(self._get_input('Enter Noise Data Rate per Host (>= 1) (in bps): ') or str(NOISE_DATA_RATE));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if NOISE_DATA_RATE < 1:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		while True:
			try:
				SAP_PORT = int(self._get_input('Enter SAP Source Port (>= 1024 & <= 65535): ') or str(SAP_PORT));
			except ValueError:
				info ('*** Error: Invalid Input\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			if SAP_PORT < 1024 or SAP_PORT > 65535:
				info ('*** Error: Input out of range\n');
				if self.cliArg['argv']:
					info ('*** Check arg #' + str(self.cliArg['cur']) + ' at Test #' + str(self.cliArg['test']) + ' in \'' + self.cliArg['test_file'] + '\'\n');
					return;
				continue;
			break;
		NOISE_PACKET_DELAY = float(8000 * gPacketConfig['MTU']) / float(NOISE_DATA_RATE);

		# Call STREAM method on Separate Thread
		if self.cliArg['argv']:
			STREAM(
				VIDEO,
				DESTINATION_RATIO,
				STREAM_IP,
				STREAM_PORT,
				NOISE_RATIO,
				NOISE_TYPE,
				NOISE_PORT,
				NOISE_DATA_RATE,
				NOISE_PACKET_DELAY,
				SAP_PORT);
		else:
			t = threading.Thread(target = STREAM, args = (
				VIDEO,
				DESTINATION_RATIO,
				STREAM_IP,
				STREAM_PORT,
				NOISE_RATIO,
				NOISE_TYPE,
				NOISE_PORT,
				NOISE_DATA_RATE,
				NOISE_PACKET_DELAY,
				SAP_PORT));
			t.start();