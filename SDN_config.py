#!/usr/bin/python

"""
	Documentation Pending
"""

import struct, socket;

# IP-INT conversion methods
IP2INT = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: socket.inet_ntoa(struct.pack('!I', n));              	# Integer to IP Address

# Maximum Transmission Unit (Bytes)
MTU = 1492;

# Protocol Overhead (18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes)
OVERHEAD = 52;		

# Stream IP & Port
STREAM_IP = '234.0.0.1';
STREAM_PORT = 5555;

# No. of Noise Switches (>= 0).
NOISE_SWITCHES = 4;

# No. of Hosts per Noise Switch (>= 0).
NOISE_HOSTS_PER_SWITCH = 2;

# Source/Destination Port to be used for Noise Packets  (1024-65535). Note: Avoid using port 5555
NOISE_SOCKET_PORT = 65535;

# Data Rate (in bps)
NOISE_DATA_RATE = 32 * 1024;

# Size of Noise Packet (in Bytes) per NOISE_PACKET_DELAY
NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;

# Delay b/w Consecutive Noise Packets (in Milliseconds).
NOISE_PACKET_DELAY = float(8000 * MTU) / float(NOISE_DATA_RATE);

# Link Speed / Interface Speed on all Switches and Hosts (in Mbps) (1-1000)
LINK_SPEED = 1;

