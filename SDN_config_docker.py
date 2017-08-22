#!/usr/bin/python

"""
    Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Input Confugration
while True:
	try:
		temp = str.upper(get_input('Enable Docker Hosts (T/F): ') or str(gDockerConfig['ENABLE'])[0]);
		if temp not in ['T', 'F']:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
	except:
		info ('*** Error: Invalid Input\n');
		if gArg['argv']:
			info ('*** Check arg #' + str(gArg['cur']) + '\n');
			Cleanup.cleanup();
			sys.exit(0);
		continue;
	gDockerConfig['ENABLE'] = (temp == 'T');
	break;
if gDockerConfig['ENABLE']:
	while True:
		try:
			temp = get_input('Enter Docker Host Image: ').strip();
			if ' ' in temp:
				info ('*** Error: Invalid Input\n');
				if gArg['argv']:
					info ('*** Check arg #' + str(gArg['cur']) + '\n');
					Cleanup.cleanup();
					sys.exit(0);
				continue;
		except:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		gDockerConfig['IMAGE'] = temp if (len(temp) > 0) else gDockerConfig['IMAGE'];
		break;
	while True:
		try:
			gDockerConfig['CPU_QUOTA'] = get_input('Enter Docker Host \'cpu-quota\' (>= -1): ') or gDockerConfig['CPU_QUOTA'];
			if isinstance(gDockerConfig['CPU_QUOTA'], str):
				gDockerConfig['CPU_QUOTA'] = int(gDockerConfig['CPU_QUOTA']);
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gDockerConfig['CPU_QUOTA'] and gDockerConfig['CPU_QUOTA'] < -1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	while True:
		try:
			gDockerConfig['CPU_PERIOD'] = get_input('Enter Docker Host \'cpu-period\' (>= -1): ') or gDockerConfig['CPU_PERIOD'];
			if isinstance(gDockerConfig['CPU_PERIOD'], str):
				gDockerConfig['CPU_PERIOD'] = int(gDockerConfig['CPU_PERIOD']);
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gDockerConfig['CPU_PERIOD'] and gDockerConfig['CPU_PERIOD'] < -1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	while True:
		try:
			gDockerConfig['CPU_SHARES'] = get_input('Enter Docker Host \'cpu-shares\' (>= -1): ') or gDockerConfig['CPU_SHARES'];
			if isinstance(gDockerConfig['CPU_SHARES'], str):
				gDockerConfig['CPU_SHARES'] = int(gDockerConfig['CPU_SHARES']);
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gDockerConfig['CPU_SHARES'] and gDockerConfig['CPU_SHARES'] < -1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	while True:
		try:
			gDockerConfig['CPUSET_CPUS'] = get_input('Enter Docker Host \'cpuset-cpus\' (0-3, 0, 1, ...): ') or gDockerConfig['CPUSET_CPUS'];
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	while True:
		try:
			gDockerConfig['MEM_LIMIT'] = get_input('Enter Docker Host \'memory\' (>= -1) (in Bytes): ') or gDockerConfig['MEM_LIMIT'];
			if isinstance(gDockerConfig['MEM_LIMIT'], str):
				gDockerConfig['MEM_LIMIT'] = int(gDockerConfig['MEM_LIMIT']);
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gDockerConfig['MEM_LIMIT'] and gDockerConfig['MEM_LIMIT'] < -1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	while True:
		try:
			gDockerConfig['MEMSWAP_LIMIT'] = get_input('Enter Docker Host \'memory-swap\' (>= -1) (in Bytes): ') or gDockerConfig['MEMSWAP_LIMIT'];
			if isinstance(gDockerConfig['MEMSWAP_LIMIT'], str):
				gDockerConfig['MEMSWAP_LIMIT'] = int(gDockerConfig['MEMSWAP_LIMIT']);
		except ValueError:
			info ('*** Error: Invalid Input\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		if gDockerConfig['MEMSWAP_LIMIT'] and gDockerConfig['MEMSWAP_LIMIT'] < -1:
			info ('*** Error: Input out of range\n');
			if gArg['argv']:
				info ('*** Check arg #' + str(gArg['cur']) + '\n');
				Cleanup.cleanup();
				sys.exit(0);
			continue;
		break;
	# while True:
	#	 try:
	#		 temp = get_input(
	#			 'Enter Docker Host Configuration\n(<cpu-quota> <cpu-period> <cpu-shares> <cpuset-cpus> <memory> <memory-swap>):\n').strip();
	#		 while temp.find('  ') > -1:
	#			 temp = temp.replace('  ', ' ');
	#		 temp = temp.split(' ');
	#		 if not temp[0]:
	#			 break;
	#		 if len(temp) != 6:
	#			 info ('*** Error: Invalid Input\n');
	#			 continue;
	#		 gDockerConfig['CPU_QUOTA'] = int(temp[0]) if (temp[0] != '-') else gDockerConfig['CPU_QUOTA'];
	#		 gDockerConfig['CPU_PERIOD'] = int(temp[1]) if (temp[1] != '-') else gDockerConfig['CPU_PERIOD'];
	#		 gDockerConfig['CPU_SHARES'] = int(temp[2]) if (temp[2] != '-') else gDockerConfig['CPU_SHARES'];
	#		 gDockerConfig['CPUSET_CPUS'] = int(temp[3]) if (temp[3] != '-') else gDockerConfig['CPUSET_CPUS'];
	#		 gDockerConfig['MEM_LIMIT'] = int(temp[4]) if (temp[4] != '-') else gDockerConfig['MEM_LIMIT'];
	#		 gDockerConfig['MEMSWAP_LIMIT'] = int(temp[5]) if (temp[5] != '-') else gDockerConfig['MEMSWAP_LIMIT'];
	#	 except ValueError:
	#		 info ('*** Error: Invalid Input\n');
	#		 continue;
	#	 break;
