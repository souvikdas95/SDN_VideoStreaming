#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Switch Count
info ('*** INFO: Only 1 Switch will be used!\n');
gConfig['SWITCH_COUNT'] = 1;

# Host Count per Switch
while True:
	try:
		gConfig['HOST_COUNT_PER_SWITCH'] = int(get_input('Enter number of hosts per switch (>= 2): ') or str(gConfig['HOST_COUNT_PER_SWITCH']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['HOST_COUNT_PER_SWITCH'] < 2:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Enable STP
# Enabling STP in 1 Switch is no use.
gConfig['USE_STP'] = False;