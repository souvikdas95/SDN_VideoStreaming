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
	import SDN_config_topology_bus;
elif gConfig['TOPOLOGY_TYPE'] == 2:
	import SDN_config_topology_ring;
elif gConfig['TOPOLOGY_TYPE'] == 3:
	import SDN_config_topology_mesh;
elif gConfig['TOPOLOGY_TYPE'] == 4:
	import SDN_config_topology_star;
elif gConfig['TOPOLOGY_TYPE'] == 5:
	import SDN_config_topology_random;
else:
	info ('*** Error: Topology Configuration doesn\'t exist!\n');
	sys.exit(0);