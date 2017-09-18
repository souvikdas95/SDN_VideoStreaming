import subprocess
import atexit;
import signal;
import shlex;
import time;
import sys;
import os;
from subprocess import Popen, PIPE;

print("*** Performing Pre-Process Cleanup");
Popen(["mn", "-c"], stdout=PIPE, stderr=PIPE, stdin=PIPE, close_fds=True).wait();

mnPath = os.getcwd() + os.path.sep + os.path.pardir;
fldPath = mnPath + os.path.sep + os.path.pardir + os.path.sep + "floodlight";

fldCmd = shlex.split("java -jar \'target" + os.path.sep + "floodlight.jar\'");

fldPid = None;
mnPid = None;

def PostCleanup():
	print("*** Performing Post-Process Cleanup");
	try:
		if fldPid is not None:
			os.kill(fldPid, signal.SIGKILL);
		if mnPid is not None:
			os.kill(mnPid, signal.SIGKILL);
	except:
		pass;
	sys.exit(0);
atexit.register(PostCleanup);
signal.signal(signal.SIGABRT, PostCleanup);
signal.signal(signal.SIGINT, PostCleanup);
signal.signal(signal.SIGSEGV, PostCleanup);
signal.signal(signal.SIGTERM, PostCleanup);

os.chdir(mnPath);

data_plane_test_cases_file = "test_cases" + os.path.sep + "data_plane_test_cases.txt";
with open(data_plane_test_cases_file, "r") as file_object:
	for line in file_object:
		print("*** Starting Floodlight Controller");
		fldProc = Popen(fldCmd, cwd = fldPath, stdout=PIPE, stderr=PIPE, stdin=PIPE, close_fds=True);
		fldPid = fldProc.pid;
		mnCmd = shlex.split("python SDN_mininet.py " + line);
		time.sleep(5);
		mnProc = Popen(mnCmd, cwd = mnPath, stdout=None, stderr=None, stdin=PIPE);
		mnPid = mnProc.pid;
		mnProc.wait();
		print("*** Stopping Floodlight Controller");
		fldProc.terminate();
