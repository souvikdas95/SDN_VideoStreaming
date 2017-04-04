#!/usr/bin/python

"""
	Documentation Pending
"""

import struct, socket;

from mininet.log import setLogLevel, info;

# IP-INT conversion methods
IP2INT = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: socket.inet_ntoa(struct.pack('!I', n));              	# Integer to IP Address

# Protocol Configuration
MTU = 1492; # Maximum Transmission Unit (Bytes)
OVERHEAD = 52;  # Protocol Overhead (18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes)

# Default Configuration (Change only if must)
TOPOLOGY_TYPE = 1;
SWITCH_COUNT = 4;
HOST_COUNT_PER_SWITCH = 2;
DESTINATION_COUNT = 1;
HOST_LINK_SPEED = 1;
SWITCH_LINK_SPEED = 1;
STREAM_IP = '234.0.0.1';
STREAM_PORT = 5555;
NOISE_PORT = 65535;
NOISE_DATA_RATE = 32 * 1024;

# Welcome
setLogLevel('info');
info('************************************\n');
info('** Welcome to SDN Video Streaming **\n');
info('************************************\n');
info('\n');

# Input Confugration
info('*** Topologies Available:\n');
info('*** 1. Bus\n');
info('*** 2. Ring\n');
info('*** 3. Mesh\n');
info('*** 4. Star\n');
while True:
    try:
        TOPOLOGY_TYPE = int(raw_input('Enter Topology: ') or str(TOPOLOGY_TYPE));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if TOPOLOGY_TYPE not in range(1, 4 + 1):
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
while True:
    try:
        MAX_DESTINATION_COUNT = SWITCH_COUNT * HOST_COUNT_PER_SWITCH - 1;
        DESTINATION_COUNT = int(raw_input('Enter number of destinations (>= 1 & <= ' + str(MAX_DESTINATION_COUNT) + '): ') or str(DESTINATION_COUNT));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if DESTINATION_COUNT not in range(1, MAX_DESTINATION_COUNT + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        SWITCH_LINK_SPEED = int(raw_input('Enter switch link speed (>= 1 & <= 1000): ') or str(SWITCH_LINK_SPEED));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if SWITCH_LINK_SPEED not in range(1, 1000 + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        HOST_LINK_SPEED = int(raw_input('Enter host link speed (>= 1 & <= 1000) (in Mbps): ') or str(HOST_LINK_SPEED));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if HOST_LINK_SPEED not in range(1, 1000 + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    STREAM_IP = IP2INT(raw_input('Enter Mutlicast Source IP: ') or STREAM_IP);
    if STREAM_IP == 0:
        info ('*** Error: Invalid Input\n');
        continue;
    if STREAM_IP not in range(IP2INT('234.0.0.1'), IP2INT('239.255.255.255') + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        STREAM_PORT = int(raw_input('Enter Mutlicast Source Port (>= 1024 & <= 65535): ') or str(STREAM_PORT));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if STREAM_PORT not in range(1024, 65535 + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        NOISE_PORT = int(raw_input('Enter Noise Source Port (>= 1024 & <= 65535): ') or str(NOISE_PORT));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if NOISE_PORT not in range(1024, 65535 + 1):
        info ('*** Error: Input out of range\n');
        continue;
    break;
while True:
    try:
        NOISE_DATA_RATE = int(raw_input('Enter Noise Data Rate (>= 1) (in bps): ') or str(NOISE_DATA_RATE));
    except ValueError:
        info ('*** Error: Invalid Input\n');
        continue;
    if NOISE_DATA_RATE < 1:
        info ('*** Error: Input out of range\n');
        continue;
    break;
NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;
NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);
