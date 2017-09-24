import subprocess;
import threading;
import atexit;
import signal;
import select;
import shlex;
import time;
import sys;
import os;
from select import poll, POLLIN;
from subprocess import Popen, PIPE, STDOUT;

def pid_exists(pid):
	try:
		os.kill(pid, 0);
	except OSError:
		return False;
	else:
		return True;

print("*** Performing Pre-Process Cleanup");
Popen(["mn", "-c"], stdout=PIPE, stderr=PIPE, stdin=PIPE, close_fds=True).wait();

mnPath = os.getcwd() + os.path.sep + os.path.pardir;
fldPath = mnPath + os.path.sep + os.path.pardir + os.path.sep + "floodlight";

fldCmd = shlex.split("java -jar \'target" + os.path.sep + "floodlight.jar\'");

fldPid = [None];
mnPid = [None];

os.chdir(mnPath);

fldLog_file = "test_cases" + os.path.sep + "floodlight.log";
fldLog = open(fldLog_file, "w");
mnLog_file = "test_cases" + os.path.sep + "mininet.log";
mnLog = open(mnLog_file, "w");

data_plane_test_cases_file = "test_cases" + os.path.sep + "data_plane_test_cases.txt";

fldLog_rfd, fldLog_wfd = os.pipe();
mnLog_rfd, mnLog_wfd = os.pipe();

gCleanup = [False];

def PostCleanup(*args, **kwargs):
	if gCleanup[0]:
		return;
	print("*** Performing Post-Process Cleanup");
	try:
		if fldPid[0] and pid_exists(fldPid[0]):
			os.kill(fldPid[0], signal.SIGTERM);
		if fldLog and not fldLog.closed:
			fldLog.close();
	except:
		pass;
	try:
		if mnPid[0] and pid_exists(mnPid[0]):
			os.kill(mnPid[0], signal.SIGTERM);
		if mnLog and not mnLog.closed:
			mnLog.close();
	except:
		pass;
	gCleanup[0] = True;
	sys.exit(0);
atexit.register(PostCleanup);
signal.signal(signal.SIGABRT, PostCleanup);
signal.signal(signal.SIGINT, PostCleanup);
signal.signal(signal.SIGSEGV, PostCleanup);
signal.signal(signal.SIGTERM, PostCleanup);

def fldLog_output(*args, **kwargs):
	_poller = poll();
	_poller.register(fldLog_rfd, POLLIN);
	while True:
		try:
			if (not fldLog) or fldLog.closed:
				break;
			if not _poller.poll(1000):
				continue;
			_output = os.read(fldLog_rfd, 1024);
			if _output != '':
				fldLog.write(_output);
				fldLog.flush();
			time.sleep(0.1);
		except:
			pass;
threading.Thread(target=fldLog_output, args=()).start();

def mnLog_output(*args, **kwargs):
	_poller = poll();
	_poller.register(mnLog_rfd, POLLIN);
	while True:
		try:
			if (not mnLog) or mnLog.closed:
				break;
			if not _poller.poll(1000):
				continue;
			_output = os.read(mnLog_rfd, 1024);
			if _output != '':
				sys.stdout.write(_output);
				sys.stdout.flush();
				mnLog.write(_output);
				mnLog.flush();
			time.sleep(0.1);
		except:
			pass;
threading.Thread(target=mnLog_output, args=()).start();

with open(data_plane_test_cases_file, "r") as file_object:
	for line in file_object:
		def _fld_thread_fn(*args, **kwargs):
			print("*** Starting Floodlight Controller");
			fldProc = Popen(fldCmd, cwd = fldPath, stdout=fldLog_wfd, stderr=STDOUT, stdin=PIPE, close_fds=True);
			fldProc.stdin.close();
			fldPid[0] = fldProc.pid;
			fldProc.wait();
			print("*** Floodlight Controller Stopped!");
		_fld_thread = threading.Thread(target=_fld_thread_fn, args=());
		_fld_thread.start();
		time.sleep(5);
		def _mn_thread_fn(*args, **kwargs):
			print("*** Starting Mininet");
			mnCmd = shlex.split("python SDN_mininet.py " + line);
			mnProc = Popen(mnCmd, cwd = mnPath, stdout=mnLog_wfd, stderr=STDOUT, stdin=PIPE, close_fds=True);
			mnProc.stdin.close();
			mnPid[0] = mnProc.pid;
			mnProc.wait();
			print("*** Mininet Stopped!");
			print("*** Stopping Floodlight Controller");
			if fldPid[0] and pid_exists(fldPid[0]):
				os.kill(fldPid[0], signal.SIGTERM);
		_mn_thread = threading.Thread(target=_mn_thread_fn, args=())
		_mn_thread.start();
		_mn_thread.join();
		_fld_thread.join();