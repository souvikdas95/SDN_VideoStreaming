#!/usr/bin/python

"""
    Documentation: Pending . . .
"""

# Global Imports
from SDN_global import *;

# Default Configuration (Change only if must)
DOCKER_ENABLE = True;
DOCKER_IMAGE = "ubuntu:build_sdn";
DOCKER_CPU_QUOTA = -1;
DOCKER_CPU_PERIOD = None;
DOCKER_CPU_SHARES = None;
DOCKER_CPUSET_CPUS = None;
DOCKER_MEM_LIMIT = None;
DOCKER_MEMSWAP_LIMIT = None;

# Input Confugration
while True:
    try:
        temp = str.upper(raw_input('Enable Docker Host Support (T/F): ') or str(DOCKER_ENABLE)[0]);
        if temp not in ['T', 'F']:
            continue;
    except:
        info ('*** Error: Invalid Input\n');
        continue;
    DOCKER_ENABLE = (temp == 'T');
    break;
if DOCKER_ENABLE:
    while True:
        try:
            temp = raw_input('Enter Docker Host Image: ').strip();
            if ' ' in temp:
                info ('*** Error: Invalid Input\n');
            DOCKER_IMAGE = temp if (len(temp) > 0) else DOCKER_IMAGE;
        except:
            info ('*** Error: Invalid Input\n');
            continue;
        break;
    while True:
        try:
            temp = raw_input(
                'Enter Docker Host Configuration\n(<cpu-quota> <cpu-period> <cpu-shares> <cpuset-cpus> <memory> <memory-swap>):\n').strip();
            while temp.find('  ') > -1:
                temp = temp.replace('  ', ' ');
            temp = temp.split(' ');
            if not temp[0]:
                break;
            if len(temp) != 6:
                info ('*** Error: Invalid Input\n');
                continue;
            DOCKER_CPU_QUOTA = int(temp[0]) if (temp[0] != '-') else DOCKER_CPU_QUOTA;
            DOCKER_CPU_PERIOD = int(temp[1]) if (temp[1] != '-') else DOCKER_CPU_PERIOD;
            DOCKER_CPU_SHARES = int(temp[2]) if (temp[2] != '-') else DOCKER_CPU_SHARES;
            DOCKER_CPUSET_CPUS = int(temp[3]) if (temp[3] != '-') else DOCKER_CPUSET_CPUS;
            DOCKER_MEM_LIMIT = int(temp[4]) if (temp[4] != '-') else DOCKER_MEM_LIMIT;
            DOCKER_MEMSWAP_LIMIT = int(temp[5]) if (temp[5] != '-') else DOCKER_MEMSWAP_LIMIT;
        except ValueError:
            info ('*** Error: Invalid Input\n');
            continue;
        break;