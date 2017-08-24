#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Switch Count
while True:
	try:
		gConfig['SWITCH_COUNT'] = int(get_input('Enter number of switches (>= 3): ') or str(gConfig['SWITCH_COUNT']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['SWITCH_COUNT'] < 3:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Host Count per Switch
while True:
	try:
		gConfig['HOST_COUNT_PER_SWITCH'] = int(get_input('Enter number of hosts per switch (>= 1): ') or str(gConfig['HOST_COUNT_PER_SWITCH']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['HOST_COUNT_PER_SWITCH'] < 1:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Enable STP
# The purpose of the topology itself is to
# contain the traffic in a single cycle
gConfig['USE_STP'] = False;

# Switch-Switch link speed
while True:
	try:
		gConfig['SWITCH_LINK_SPEED'] = float(get_input('Enter switch-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(gConfig['SWITCH_LINK_SPEED']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['SWITCH_LINK_SPEED'] < 1 or gConfig['SWITCH_LINK_SPEED'] > 1000:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

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