#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# System Imports
import sys, os, threading, time, math, random, csv;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

# Mininet Imports
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel, info, warn;
from mininet.node import Node;
from mininet.util import waitListening;
from mininet.node import OVSSwitch, Controller, RemoteController;
from mininet.link import OVSLink;
from mininet.link import OVSIntf;
from mininet.link import TCLink;
from mininet.link import TCIntf;
from mininet.clean import Cleanup;

# Import SDN Utils
from SDN_utils import makedirs_s, IP2INT, INT2IP;

# Base Directory
BASE_DIR = os.path.dirname(os.path.realpath(__file__));

# Add BASE_DIR to PYTHONPATH
sys.path.append(BASE_DIR);

# Check for Commandline arguments
gArg = {
	'argv' : None,
	'cur' : 0,
};

# Method to get config input from usable source
def get_input(_str):
	if gArg['argv']:
		if gArg['cur'] < len(gArg['argv']) - 2:
			gArg['cur'] += 1;
			_input = gArg['argv'][gArg['cur']];
		else:
			_input = '';
	else:
		_input = raw_input(_str);
	return _input;

# Outsourced Default Locals from __main__
gMain = {
	'switch_list' : [],
	'switch_count' : 0,
	'switch_host_list' : [],
	'host_list' : [],
	'host_count' : 0,
	'host_volumes' : [],
	'switch_switch_link_list' : [],
};

# Mininet Default Configuration
gConfig = {
	'TOPOLOGY_LIST' : ['Bus', 'Ring', 'Mesh', 'Star', 'Random'],
	'TOPOLOGY_TYPE' : 1,
	'SWITCH_COUNT' : 4,
	'HOST_COUNT_PER_SWITCH' : 2,
	'SWITCH_GLOBAL_MAX_LINKS' : 3,
	'USE_STP' : False,
	'HOST_LINK_SPEED' : 1,
	'SWITCH_LINK_SPEED' : 1,
};

# Docker Default Configuration
gDockerConfig = {
	'ENABLE' : False,
	'IMAGE' : 'ubuntu:build_sdn',
	'CPU_QUOTA' : -1,
	'CPU_PERIOD' : None,
	'CPU_SHARES' : None,
	'CPUSET_CPUS' : None,
	'MEM_LIMIT' : None,
	'MEMSWAP_LIMIT' : None,
};

# Packet Default Configuration
gPacketConfig = {
	# Maximum Transmission Unit (Bytes)
	'MTU' : 1492,
	# Protocol Overhead (18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes)
	'OVERHEAD' : 52,
	# Ensure Full Utilization of Packet (MTU - OVERHEAD)
	'NOISE_PACKET_PAYLOAD_SIZE' : 1440,
};

# Stream Default Configuration
gStreamConfig = {
	'SOURCE' : 'samples' + os.path.sep + 'sample1.avi',
	'DESTINATION_COUNT' : 1,
	'STREAM_IP' : IP2INT('234.0.0.1'),
	'STREAM_PORT' : 5555,
	'NOISE_TYPE' : 1,
	'NOISE_DESTINATION_PORT' : 65535,
	'NOISE_DATA_RATE' : 32 * 1024,
	'NOISE_PACKET_DELAY' : 364.2578125,
	'SAP_PORT' : 49160,
};