#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Switch Count
while True:
	try:
		gConfig['SWITCH_COUNT'] = int(get_input('Enter number of switches (>= 2): ') or str(gConfig['SWITCH_COUNT']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['SWITCH_COUNT'] < 2:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;
	
# Max. Hosts Per Switch
while True:
	try:
		gConfig['HOST_COUNT_PER_SWITCH'] = int(get_input('Enter max. hosts per switch (>= 1): ') or str(gConfig['HOST_COUNT_PER_SWITCH']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['HOST_COUNT_PER_SWITCH'] < 1:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Total Host Count in Topology
while True:
	try:
		gConfig['RANDOM_TOTAL_HOST_COUNT'] = int(get_input('Enter Total Host Count in Topology (>= 2 & <= ' + str(gConfig['SWITCH_COUNT'] * gConfig['HOST_COUNT_PER_SWITCH']) + '): ') or str(gConfig['RANDOM_TOTAL_HOST_COUNT']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['RANDOM_TOTAL_HOST_COUNT'] < 2:
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Switch Global Max Links
while True:
	try:
		gConfig['SWITCH_GLOBAL_MAX_LINKS'] = int(get_input('Enter Global max. Switch-Switch links (>= ' + str(gConfig['SWITCH_COUNT'] - 1) + ' & <= ' + str((gConfig['SWITCH_COUNT'] - 1) * gConfig['SWITCH_COUNT'] / 2) + '): ') or str(2 * (gConfig['SWITCH_COUNT'] - 1)));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['SWITCH_GLOBAL_MAX_LINKS'] < (gConfig['SWITCH_COUNT'] - 1) or gConfig['SWITCH_GLOBAL_MAX_LINKS'] > ((gConfig['SWITCH_COUNT'] - 1) * gConfig['SWITCH_COUNT'] / 2):
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;

# Enable STP
while True:
	try:
		temp = str.upper(get_input('Enable STP (T/F): ') or str(gConfig['USE_STP'])[0]);
		if temp not in ['T', 'F']:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
	except:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	gConfig['USE_STP'] = (temp == 'T');
	break;

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