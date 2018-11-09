#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# System Imports
import sys, os, threading, time, math, random, csv, signal, atexit, urllib2, shlex, pipes, json;

# Subprocess utils
from subprocess import Popen, PIPE;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

# Mininet Imports
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel, info as unsafeInfo, warn as unsafeWarn;
from mininet.node import Node;
from mininet.util import waitListening;
from mininet.node import OVSSwitch, Controller, RemoteController;
from mininet.link import OVSLink;
from mininet.link import OVSIntf;
from mininet.link import TCLink;
from mininet.link import TCIntf;
from mininet.clean import Cleanup;

# Wrap and override unsafe logging methods
logMutex = threading.Lock()

def info(*args, **kwargs):
	logMutex.acquire();
	unsafeInfo(*args, **kwargs);
	logMutex.release();

def warn(*args, **kwargs):
	logMutex.acquire();
	unsafeWarn(*args, **kwargs);
	logMutex.release();

# Import SDN Utils
from SDN_utils import makedirs_s, get_mean, IP2INT, INT2IP;

# Base Directory
BASE_DIR = os.path.dirname(os.path.realpath(__file__));

# Add BASE_DIR to PYTHONPATH
sys.path.append(BASE_DIR);

# Topology Directory
TOPOLOGY_DIR = BASE_DIR + os.path.sep + 'topology';

# Add TOPOLOGY_DIR to PYTHONPATH
sys.path.append(TOPOLOGY_DIR);

# Check for redundant Cleanup
gCleanup = [False];

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

# Declare Outsourced Locals for __main__
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
	# All Config Params
	'SWITCH_COUNT' : 4,
	'HOST_COUNT_PER_SWITCH' : 2,
	'USE_STP' : False,
	'SWITCH_LINK_SPEED' : 1,
	'HOST_LINK_SPEED' : 1,
	# Random Config Params
	'RANDOM_SWITCH_GLOBAL_MAX_LINKS' : 3,
	'RANDOM_TOTAL_HOST_COUNT' : 2,
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
	'VIDEO' : 'videos' + os.path.sep + 'bus' + os.path.sep + 'bus000.avi',
	'DESTINATION_RATIO' : 0.25,
	'STREAM_IP' : IP2INT('225.225.0.1'),
	'STREAM_PORT' : 5555,
	'NOISE_TYPE' : 1,
	'NOISE_RATIO' : 0.5,
	'NOISE_PORT' : 65535,
	'NOISE_DATA_RATE' : 32 * 1024,
	'NOISE_PACKET_DELAY' : 364.2578125,
	'SAP_PORT' : 49160,
};

# Dictionary of Global Mutex
gMutex = {
	'STREAM_INIT' : threading.Lock(),
	'STREAM_END' : threading.Lock(),
	'SUBPROCESS' : threading.Lock(),
}
