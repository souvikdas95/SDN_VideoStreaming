#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

if __name__ == "__main__":
	""" This is the Main
	    Method of SDN_VideoStreaming """
	# Get Argv
	gArg['argv'] = sys.argv;
	if len(gArg['argv']) < 2:
		gArg['argv'] = None;
	else:
		gStreamConfig['SOURCE'] = gArg['argv'][-1];

	# Initiate SDN Base Configuration
	import SDN_config;

	# Docker Support Check
	try:
		# Import Docker Host Class
		from mininet.node import Docker;
	except ImportError:
		gDockerConfig['ENABLE'] = False;
	else:
		# Initiate SDN Docker Configuration
		import SDN_config_docker;

	# Import CustomCLI Class
	from SDN_CustomCLI import CustomCLI;

	# Create Mininet Instance
	setLogLevel('info');
	net = Mininet(topo = None, controller = None, build = False, waitConnected = True);

	# Connect to Controller
	info('*** Connecting to controller\n');
	net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6653, ipBase = '10.0.0.128');

	# Declare IP Pool
	info('*** Declaring IP Pool\n');
	iter_ip = IP2INT('10.0.0.128'); # Starting Address

	# Create Switches
	info('*** Creating switches (Open vSwitch w/ OpenFlow13)\n');
	for i in range(gConfig['SWITCH_COUNT']):
		gMain['switch_count'] += 1;
		gMain['switch_list'].append(net.addSwitch('s' + str(gMain['switch_count']), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False,
							failMode = 'standalone' if (gConfig['USE_STP'] == True) else 'secure',
							stp = gConfig['USE_STP']));

	# Create Hosts
	info('*** Creating hosts\n');
	host_count_in_switch = gConfig['HOST_COUNT_PER_SWITCH'];
	if gDockerConfig['ENABLE']:
		gMain['host_volumes'].append(BASE_DIR + ':' + BASE_DIR);
		for i in range(gConfig['SWITCH_COUNT']):
			gMain['switch_host_list'].append([]);
			if gConfig['TOPOLOGY_TYPE'] == 5:
				host_count_in_switch = random.randint(0, gConfig['HOST_COUNT_PER_SWITCH']);
			for j in range(host_count_in_switch):
				gMain['host_count'] += 1;
				h = net.addHost('d' + str(gMain['host_count']), ip = INT2IP(iter_ip),
					cls = Docker,
					dimage = gDockerConfig['IMAGE'],
					cpu_quota = gDockerConfig['CPU_QUOTA'],
					cpu_period = gDockerConfig['CPU_PERIOD'],
					cpu_shares = gDockerConfig['CPU_SHARES'],
					cpuset_cpus = gDockerConfig['CPUSET_CPUS'],
					mem_limit = gDockerConfig['MEM_LIMIT'],
					memswap_limit = gDockerConfig['MEMSWAP_LIMIT'],
					volumes = gMain['host_volumes']);
				gMain['switch_host_list'][i].append(h);
				gMain['host_list'].append(h);
				iter_ip += 1;
	else:
		for i in range(gConfig['SWITCH_COUNT']):
			gMain['switch_host_list'].append([]);
			if gConfig['TOPOLOGY_TYPE'] == 5:
				host_count_in_switch = random.randint(0, gConfig['HOST_COUNT_PER_SWITCH']);
			for j in range(host_count_in_switch):
				gMain['host_count'] += 1;
				h = net.addHost('h' + str(gMain['host_count']), ip = INT2IP(iter_ip));
				gMain['switch_host_list'][i].append(h);
				gMain['host_list'].append(h);
				iter_ip += 1;

	# Create Switch - Switch Links
	info('*** Creating Switch - Switch Links\n');
	if gConfig['TOPOLOGY_TYPE'] == 1:
		for i in range(gConfig['SWITCH_COUNT'] - 1):
			gMain['switch_switch_link_list'].append(net.addLink(gMain['switch_list'][i], gMain['switch_list'][i + 1], cls = TCLink, Intf = TCIntf, fast = False));
	elif gConfig['TOPOLOGY_TYPE'] == 2:
		for i in range(gConfig['SWITCH_COUNT'] - 1):
			gMain['switch_switch_link_list'].append(net.addLink(gMain['switch_list'][i], gMain['switch_list'][i + 1], cls = TCLink, Intf = TCIntf, fast = False));
		gMain['switch_switch_link_list'].append(net.addLink(gMain['switch_list'][gConfig['SWITCH_COUNT'] - 1], gMain['switch_list'][0], cls = TCLink, Intf = TCIntf, fast = False));
	elif gConfig['TOPOLOGY_TYPE'] == 3:
		for i in range(gConfig['SWITCH_COUNT'] - 1):
			for j in range(i + 1, gConfig['SWITCH_COUNT']):
				gMain['switch_switch_link_list'].append(net.addLink(gMain['switch_list'][i], gMain['switch_list'][j], cls = TCLink, Intf = TCIntf, fast = False));
	elif gConfig['TOPOLOGY_TYPE'] == 4:
		pass; # Nothing to do with 1 Switch :V
	elif gConfig['TOPOLOGY_TYPE'] == 5:
		neighbor = {};
		switch_switch_link_selection_list = list();
		for i in range(gConfig['SWITCH_COUNT'] - 1):
			if neighbor.has_key(gMain['switch_list'][i]) == False:
				neighbor[gMain['switch_list'][i]] = set();
			for j in range(i + 1, gConfig['SWITCH_COUNT']):
				if neighbor.has_key(gMain['switch_list'][j]) == False:
					neighbor[gMain['switch_list'][j]] = set();
				switch_switch_link_selection_list.append((i, j));
		# Note: Max. Links to allocate via Random from list must
		# always be less than Max. Global Switch links by an amount,
		# equal to (gConfig['SWITCH_COUNT'] - 1).
		switch_switch_link_selection_list = random.sample(switch_switch_link_selection_list, gConfig['SWITCH_GLOBAL_MAX_LINKS'] - (gConfig['SWITCH_COUNT'] - 1));
		for (i, j) in switch_switch_link_selection_list:
			gMain['switch_switch_link_list'].append(net.addLink(gMain['switch_list'][i], gMain['switch_list'][j], cls = TCLink, Intf = TCIntf, fast = False));
			neighbor[gMain['switch_list'][i]].add(gMain['switch_list'][j]);
			neighbor[gMain['switch_list'][j]].add(gMain['switch_list'][i]);
		conn_comp_list = [];
		switch_set = set(gMain['switch_list']);
		while switch_set:
			sw = switch_set.pop();
			group_set = {sw};
			queue_list = [sw];
			while queue_list:
				sw = queue_list.pop(0);
				neighbor_set = neighbor[sw];
				neighbor_set.difference_update(group_set);
				switch_set.difference_update(neighbor_set);
				group_set.update(neighbor_set);
				queue_list.extend(neighbor_set);
			conn_comp_list.append(group_set);
		# for i in range(len(conn_comp_list)):
		# 	info("Component #" + str(i + 1) + ": ");
		# 	jlist = list(conn_comp_list[i]);
		# 	for j in range(len(jlist)):
		# 		info(jlist[j].name + ", ");
		# 	print("\n");
		for i in range(len(conn_comp_list) - 1):
			rand_comp_item1 = random.sample(conn_comp_list[i], 1)[0];
			rand_comp_item2 = random.sample(conn_comp_list[i + 1], 1)[0];
			gMain['switch_switch_link_list'].append(net.addLink(rand_comp_item1, rand_comp_item2, cls = TCLink, Intf = TCIntf, fast = False));

	# Create Switch - Host Links
	info('*** Creating Switch - Host Links\n');
	switch_host_link_list = [];
	for i in range(gConfig['SWITCH_COUNT']):
		switch_host_link_list.append([]);
		for j in range(len(gMain['switch_host_list'][i])):
			switch_host_link_list[i].append(net.addLink(gMain['switch_list'][i], gMain['switch_host_list'][i][j], cls = TCLink, Intf = TCIntf, fast = False));

	# Start Network
	info('*** Starting Network\n');
	net.start();

	# Configure Traffic Control on Switch - Switch Interfaces
	if gConfig['TOPOLOGY_TYPE'] != 4:
		info('*** Configuring Traffic Control on Switch - Switch Interfaces\n');
		setLogLevel('error');
		for i in range(len(gMain['switch_switch_link_list'])):
			gMain['switch_switch_link_list'][i].intf1.config(bw = gConfig['SWITCH_LINK_SPEED']);
			gMain['switch_switch_link_list'][i].intf2.config(bw = gConfig['SWITCH_LINK_SPEED']);
		setLogLevel('info');

	# Configure Traffic Control on Switch - Host Interfaces
	info('*** Configuring Traffic Control on Switch - Host Interfaces\n');
	setLogLevel('error');
	for i in range(gConfig['SWITCH_COUNT']):
		for j in range(len(switch_host_link_list[i])):
			switch_host_link_list[i][j].intf1.config(bw = gConfig['HOST_LINK_SPEED']);
			switch_host_link_list[i][j].intf2.config(bw = gConfig['HOST_LINK_SPEED']);
	setLogLevel('info');

	# Configure Host Default Routes
	info('*** Configuring Host Default Routes\n');
	for i in range(len(gMain['host_list'])):
		gMain['host_list'][i].setDefaultRoute(gMain['host_list'][i].defaultIntf());

	# Switch to CLI
	CustomCLI(net);

	# Stop Network
	info('*** Stopping Network\n');
	net.stop();

	# Cleanup
	info('*** Cleaning Up\n');
	Cleanup.cleanup();