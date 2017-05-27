"""
	Input: HostIP, HostPort, FileLoadLocation
"""
import socket;
import sys;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

from SAP_class import SAP;

# Read Args
argv = sys.argv;

# Read File
fr = open(argv[3], "r");
sdp = fr.read(1024);
fr.close();

# Wait for Request
host_ip = argv[1];
host_port = int(argv[2]);
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((host_ip, host_port));
while True:
	msg, sender = sock.recvfrom(1024);
	sap = SAP.parseMessage(msg);
	sap.set_Payload(sdp);
	msg = sap.generateMessage();
	sock.sendto(msg, sender);
