"""
	Input: HostIP, HostPort, FileSaveLocation
"""
import socket;
import threading;
import time;
import sys;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

from SAP_class import SAP;

# Get Next Hop IP Address using Destination IP
def GetNextHopIPfromDestinationIP(host_ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
	s.connect((host_ip, 0));
	return s.getsockname()[0];

# Read Args
argv = sys.argv;

# Send Request
host_ip = argv[1];
host_port = int(argv[2]);
sap = SAP();
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sap.srcIP = GetNextHopIPfromDestinationIP(host_ip);
msg = sap.generateMessage();
def _sendto(_sock, _msg, (_host_ip, _host_port)):
	while True:
		try:
			_sock.sendto(_msg, (_host_ip, _host_port));
		except:
			return;
		time.sleep(1);	# Retry every 1 Second
thread_sendto = threading.Thread(target=_sendto, args=(sock, msg, (host_ip, host_port)));
thread_sendto.start();

# Receive Response
msg, sender = sock.recvfrom(1024); # Hope 1024 buffer size will be sufficient
while sender != (host_ip, host_port):
	msg, sender = sock.recvfrom(1024);
sock.close();
sap = SAP.parseMessage(msg);
sdp = sap.get_Payload();
fw = open(argv[3], "w");
fw.write(sdp);
fw.close();

	

