#!/usr/bin/python

"""
	Documentation Pending
"""

import struct, socket;

from mininet.log import setLogLevel, info;

# Default Configuration (Change only if must)
TOPOLOGY_TYPE = 1;
SWITCH_COUNT = 4;
HOST_COUNT_PER_SWITCH = 2;
USE_STP = False;
HOST_LINK_SPEED = 1;
SWITCH_LINK_SPEED = 1;

# Welcome
setLogLevel('info');
info('************************************\n');
info('** Welcome to SDN Video Streaming **\n');
info('************************************\n');
info('\n');

# Input Confugration
TOPOlOGY_LIST = ['Bus', 'Ring', 'Mesh', 'Star', 'Random'];
info('*** Topologies Available:\n');
info('*** 1. Bus\n');
info('*** 2. Ring\n');
info('*** 3. Mesh\n');
info('*** 4. Star\n');
info('*** 5. Random\n');
while True:
    try:
        TOPOLOGY_TYPE = int(raw_input('Enter Topology: ') or str(TOPOLOGY_TYPE));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if TOPOLOGY_TYPE not in range(1, 5 + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
if TOPOLOGY_TYPE == 1:
    while True:
        try:
            SWITCH_COUNT = int(raw_input('Enter number of switches (>= 2): ') or str(SWITCH_COUNT));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if SWITCH_COUNT < 2:
            info ('*** Error: Input out of range\n');
            continue;
        break;
    while True:
        try:
            HOST_COUNT_PER_SWITCH = int(raw_input('Enter number of hosts per switch (>= 1): ') or str(HOST_COUNT_PER_SWITCH));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if HOST_COUNT_PER_SWITCH < 1:
            info ('*** Error: Input out of range\n');
            continue;
        break;
elif TOPOLOGY_TYPE == 2:
    while True:
        try:
            SWITCH_COUNT = int(raw_input('Enter number of switches (>= 3): ') or str(SWITCH_COUNT));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if SWITCH_COUNT < 3:
            info ('*** Error: Invalid Input\n');
            continue;
        break;
    while True:
        try:
            HOST_COUNT_PER_SWITCH = int(raw_input('Enter number of hosts per switch (>= 1): ') or str(HOST_COUNT_PER_SWITCH));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if HOST_COUNT_PER_SWITCH < 1:
            info ('*** Error: Invalid Input\n');
            continue;
        break;
elif TOPOLOGY_TYPE == 3:
    while True:
        try:
            SWITCH_COUNT = int(raw_input('Enter number of switches (>= 4): ') or str(SWITCH_COUNT));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if SWITCH_COUNT < 4:
            info ('*** Error: Input out of range\n');
            continue;
        break;
    while True:
        try:
            HOST_COUNT_PER_SWITCH = int(raw_input('Enter number of hosts per switch (>= 1): ') or str(HOST_COUNT_PER_SWITCH));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if HOST_COUNT_PER_SWITCH < 1:
            info ('*** Error: Input out of range\n');
            continue;
        break;
elif TOPOLOGY_TYPE == 4:
    info ('*** INFO: Only 1 Switch will be used!\n');
    SWITCH_COUNT = 1;   
    while True:
        try:
            HOST_COUNT_PER_SWITCH = int(raw_input('Enter number of hosts per switch (>= 2): ') or str(HOST_COUNT_PER_SWITCH));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if HOST_COUNT_PER_SWITCH < 2:
            info ('*** Error: Input out of range\n');
            continue;
        break;
elif TOPOLOGY_TYPE == 5:
    while True:
        try:
            SWITCH_COUNT = int(raw_input('Enter number of switches (>= 1): ') or str(SWITCH_COUNT));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if SWITCH_COUNT < 1:
            info ('*** Error: Input out of range\n');
            continue;
        break;
    while True:
        try:
            HOST_COUNT_PER_SWITCH = int(raw_input('Enter max. hosts per switch (>= 1): ') or str(HOST_COUNT_PER_SWITCH));
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        if HOST_COUNT_PER_SWITCH < 1:
            info ('*** Error: Input out of range\n');
            continue;
        break;
while True:
	try:
		temp = str.upper(raw_input('Enable STP (T/F): ') or str(USE_STP)[0]);
		if temp not in ['T', 'F']:
			continue;
	except:
		info ('*** Error: Invalid Input\n');
		continue;
	USE_STP = (temp == 'T');
	break;
while True:
    try:
        SWITCH_LINK_SPEED = int(raw_input('Enter switch-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(SWITCH_LINK_SPEED));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if SWITCH_LINK_SPEED < 1 or SWITCH_LINK_SPEED > 1000:
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        HOST_LINK_SPEED = int(raw_input('Enter host-switch link speed (>= 1 & <= 1000) (in Mbps): ') or str(HOST_LINK_SPEED));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if HOST_LINK_SPEED < 1 or HOST_LINK_SPEED > 1000:
        info ('*** Error: Input out of range\n');
        continue;
    break;
