import subprocess
import shlex;
import sys;
import os;
from subprocess import Popen, PIPE;

os.chdir("..");

data_plane_test_cases_file = "test_cases/data_plane_test_cases.txt";

with open(data_plane_test_cases_file, "r") as file_object:
	for line in file_object:
		cmd = shlex.split("python SDN_mininet.py " + line);
		proc = Popen(cmd, stdout=PIPE);
		for c in iter(lambda: proc.stdout.read(1), ''):
		    sys.stdout.write(c);
