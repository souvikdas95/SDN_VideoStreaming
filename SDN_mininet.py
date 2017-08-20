#!/usr/bin/python

"""
	Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Import CustomCLI
from SDN_CustomCLI import CustomCLI;

if __name__ == "__main__":
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
	for i in range(SWITCH_COUNT):
	    switch_count += 1;
	    switch_list.append(net.addSwitch('s' + str(switch_count), cls = OVSSwitch, protocols = 'OpenFlow13', inband = False,
	    					failMode = 'standalone' if (USE_STP == True) else 'secure',
	    					stp = USE_STP));

	# Create Hosts
	info('*** Creating hosts\n');
	host_count_in_switch = HOST_COUNT_PER_SWITCH;
	if DOCKER_ENABLE:
		host_volumes.append(BASE_DIR + ':' + BASE_DIR);
		for i in range(SWITCH_COUNT):
			switch_host_list.append([]);
			if TOPOLOGY_TYPE == 5:
				host_count_in_switch = random.randint(0, HOST_COUNT_PER_SWITCH);
			for j in range(host_count_in_switch):
				host_count += 1;
				h = net.addHost('d' + str(host_count), ip = INT2IP(iter_ip),
					cls = Docker,
					dimage = DOCKER_IMAGE,
					cpu_quota = DOCKER_CPU_QUOTA,
		            cpu_period = DOCKER_CPU_PERIOD,
		            cpu_shares = DOCKER_CPU_SHARES,
		            cpuset_cpus = DOCKER_CPUSET_CPUS,
		            mem_limit = DOCKER_MEM_LIMIT,
		            memswap_limit = DOCKER_MEMSWAP_LIMIT,
					volumes = host_volumes);
				switch_host_list[i].append(h);
				host_list.append(h);
				iter_ip += 1;
	else:
		for i in range(SWITCH_COUNT):
			switch_host_list.append([]);
			if TOPOLOGY_TYPE == 5:
				host_count_in_switch = random.randint(0, HOST_COUNT_PER_SWITCH);
			for j in range(host_count_in_switch):
				host_count += 1;
				h = net.addHost('h' + str(host_count), ip = INT2IP(iter_ip));
				switch_host_list[i].append(h);
				host_list.append(h);
				iter_ip += 1;

	# Create Switch - Switch Links
	info('*** Creating Switch - Switch Links\n');
	if TOPOLOGY_TYPE == 1:
	    for i in range(SWITCH_COUNT - 1):
	        switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[i + 1], cls = TCLink, Intf = TCIntf, fast = False));
	elif TOPOLOGY_TYPE == 2:
	    for i in range(SWITCH_COUNT - 1):
	        switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[i + 1], cls = TCLink, Intf = TCIntf, fast = False));
	    switch_switch_link_list.append(net.addLink(switch_list[SWITCH_COUNT - 1], switch_list[0], cls = TCLink, Intf = TCIntf, fast = False));
	elif TOPOLOGY_TYPE == 3:
	    for i in range(SWITCH_COUNT - 1):
	        for j in range(i + 1, SWITCH_COUNT):
	            switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[j], cls = TCLink, Intf = TCIntf, fast = False));
	elif TOPOLOGY_TYPE == 4:
	    pass; # Nothing to do with 1 Switch :V
	elif TOPOLOGY_TYPE == 5:
		neighbor = {};
		switch_switch_link_selection_list = list();
		for i in range(SWITCH_COUNT - 1):
			if neighbor.has_key(switch_list[i]) == False:
				neighbor[switch_list[i]] = set();
			for j in range(i + 1, SWITCH_COUNT):
				if neighbor.has_key(switch_list[j]) == False:
					neighbor[switch_list[j]] = set();
				switch_switch_link_selection_list.append((i, j));
		# Note: Max. Links to allocate via Random from list must
		# always be less than Max. Global Switch links by an amount,
		# equal to (SWITCH_COUNT - 1).
		switch_switch_link_selection_list = random.sample(switch_switch_link_selection_list, SWITCH_GLOBAL_MAX_LINKS - (SWITCH_COUNT - 1));
		for (i, j) in switch_switch_link_selection_list:
			switch_switch_link_list.append(net.addLink(switch_list[i], switch_list[j], cls = TCLink, Intf = TCIntf, fast = False));
			neighbor[switch_list[i]].add(switch_list[j]);
			neighbor[switch_list[j]].add(switch_list[i]);
		conn_comp_list = [];
		switch_set = set(switch_list);
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
			switch_switch_link_list.append(net.addLink(rand_comp_item1, rand_comp_item2, cls = TCLink, Intf = TCIntf, fast = False));

	# Create Switch - Host Links
	info('*** Creating Switch - Host Links\n');
	switch_host_link_list = [];
	for i in range(SWITCH_COUNT):
		switch_host_link_list.append([]);
		for j in range(len(switch_host_list[i])):
			switch_host_link_list[i].append(net.addLink(switch_list[i], switch_host_list[i][j], cls = TCLink, Intf = TCIntf, fast = False));

	# Start Network
	info('*** Starting Network\n');
	net.start();

	# Configure Traffic Control on Switch - Switch Interfaces
	if TOPOLOGY_TYPE != 4:
	    info('*** Configuring Traffic Control on Switch - Switch Interfaces\n');
	    setLogLevel('error');
	    for i in range(len(switch_switch_link_list)):
	        switch_switch_link_list[i].intf1.config(bw = SWITCH_LINK_SPEED);
	        switch_switch_link_list[i].intf2.config(bw = SWITCH_LINK_SPEED);
	    setLogLevel('info');

	# Configure Traffic Control on Switch - Host Interfaces
	info('*** Configuring Traffic Control on Switch - Host Interfaces\n');
	setLogLevel('error');
	for i in range(SWITCH_COUNT):
		for j in range(len(switch_host_link_list[i])):
			switch_host_link_list[i][j].intf1.config(bw = HOST_LINK_SPEED);
			switch_host_link_list[i][j].intf2.config(bw = HOST_LINK_SPEED);
	setLogLevel('info');

	# Configure Host Default Routes
	info('*** Configuring Host Default Routes\n');
	for i in range(len(host_list)):
	    host_list[i].setDefaultRoute(host_list[i].defaultIntf());

	# Switch to CLI
	CustomCLI(net);

	# Stop Network
	info('*** Stopping Network\n');
	net.stop();

	# Cleanup
	info('*** Cleaning Up\n');
	Cleanup.cleanup();