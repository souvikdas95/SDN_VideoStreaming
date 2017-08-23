#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Welcome
setLogLevel('info');
info('************************************\n');
info('** Welcome to SDN Video Streaming **\n');
info('************************************\n');
info('\n');

# Input Confugration
_topo_msg = '*** Topologies Available:\n';
for i in range(len(gConfig['TOPOLOGY_LIST'])):
	_topo_msg += '*** ' + str(i + 1) + '. ' + gConfig['TOPOLOGY_LIST'][i] + '\n';
while True:
	try:
		gConfig['TOPOLOGY_TYPE'] = int(get_input(_topo_msg + 'Enter Topology: ') or str(gConfig['TOPOLOGY_TYPE']));
	except ValueError:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	if gConfig['TOPOLOGY_TYPE'] not in range(1, len(gConfig['TOPOLOGY_LIST']) + 1):
		info ('*** Error: Input out of range\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	break;
if gConfig['TOPOLOGY_TYPE'] == 1:
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
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
elif gConfig['TOPOLOGY_TYPE'] == 2:
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
elif gConfig['TOPOLOGY_TYPE'] == 3:
	while True:
		try:
			gConfig['SWITCH_COUNT'] = int(get_input('Enter number of switches (>= 4): ') or str(gConfig['SWITCH_COUNT']));
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gConfig['SWITCH_COUNT'] < 4:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
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
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
elif gConfig['TOPOLOGY_TYPE'] == 4:
	info ('*** INFO: Only 1 Switch will be used!\n');
	gConfig['SWITCH_COUNT'] = 1;   
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
elif gConfig['TOPOLOGY_TYPE'] == 5:
	while True:
		try:
			gConfig['SWITCH_COUNT'] = int(get_input('Enter number of switches (>= 1): ') or str(gConfig['SWITCH_COUNT']));
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gConfig['SWITCH_COUNT'] < 1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
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
if gConfig['TOPOLOGY_TYPE'] != 4:
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
	while True:
		try:
			gConfig['SWITCH_LINK_SPEED'] = int(get_input('Enter switch-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(gConfig['SWITCH_LINK_SPEED']));
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
while True:
	try:
		gConfig['HOST_LINK_SPEED'] = int(get_input('Enter host-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(gConfig['HOST_LINK_SPEED']));
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