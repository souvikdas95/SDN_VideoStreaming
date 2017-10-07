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
host_ip = argv[1];
host_port = int(argv[2]);

# Read File
fr = open(argv[3], "r");
sdp = fr.read(4096);
fr.close();

# Wait for Request
sys.stdout.write("Listening for SAP Requests on \'" + str(host_ip) + ":" + str(host_port) + "\'\n");
sys.stdout.flush();
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((host_ip, host_port));
while True:
	try:
		msg, sender = sock.recvfrom(4096);
		sys.stdout.write("Received Request from \'" + str(sender[0]) + ":" + str(sender[1]) + "\'\n");
		sys.stdout.flush();
		sap = SAP.parseMessage(msg);
		sap.set_Payload(sdp);
		msg = sap.generateMessage();
		sock.sendto(msg, sender);
	except Exception as e:
		sys.stdout.write('ERROR: ' + str(e) + '\n');
		sys.stdout.flush();

