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

# Switch-Switch Link speed
# With 1 switch, this configuration doesn't matter
gConfig['SWITCH_LINK_SPEED'] = 1;

# Host-Switch link speed
while True:
	try:
		gConfig['HOST_LINK_SPEED'] = float(get_input('Enter host-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(gConfig['HOST_LINK_SPEED']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['HOST_LINK_SPEED'] < 1 or gConfig['HOST_LINK_SPEED'] > 1000:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;