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

# Find Mean
def get_mean(_list):
	if not _list:
		return 0.0;
	_list = map(lambda x: x if x >= 0 else 0, _list);	# Force -ve Values to Zero (Error Codes)
	return sum(_list) / len(_list);

# Find Median
def get_median(_list):
	if not _list:
		return 0.0;
	_list = sorted(map(lambda x: x if x >= 0 else 0, _list));	# Force -ve Values to Zero (Error Codes) and Sort the list
	_len = len(_list);
	if (_len % 2) == 1:
		return _list[_len / 2];
	return (_list[(_len / 2) - 1] + _list[_len / 2]) / 2;