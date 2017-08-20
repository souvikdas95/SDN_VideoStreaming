#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# System Imports
import sys, os, threading, time, math, random, csv, struct, socket;

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

# Base Directory
BASE_DIR = os.path.dirname(os.path.realpath(__file__));

# Add BASE_DIR to PYTHONPATH
sys.path.append(BASE_DIR);

# Import SDN Utils
from SDN_utils import makedirs_s, IP2INT, INT2IP;

# Import SDN Base Configuration
from SDN_config import *;

# Docker Support Check
try:
	from mininet.node import Docker;
except ImportError:
	DOCKER_ENABLE = False;
else:
	# Import SDN Docker Configuration
	from SDN_config_docker import *;

# Packet Configuration Defaults for Mininet
MTU = 1492; # Maximum Transmission Unit (Bytes)
OVERHEAD = 52;  # Protocol Overhead (18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes)
NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;	# Ensure Full Utilization of Packet

# Outsourced Locals from __main__
switch_list = [];
switch_count = 0;
switch_host_list = [];
host_list = [];
host_count = 0;
host_volumes = [];
switch_switch_link_list = [];