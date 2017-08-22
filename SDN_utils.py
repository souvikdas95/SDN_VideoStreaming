#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
import os, socket, struct;

# Make Directories Save (Create if not exists)
def makedirs_s(s):
	if os.path.exists(s) is False:
		os.makedirs(s);

# IP-INT conversion methods
IP2INT = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: socket.inet_ntoa(struct.pack('!I', n));					# Integer to IP Address