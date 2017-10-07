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
host_ip = argv[1];
host_port = int(argv[2]);

# Send Request
sys.stdout.write("Sending SAP Request to SAP Server @ \'" + str(host_ip) + ":" + str(host_port) + "\'\n");
sys.stdout.flush();
sap = SAP();
sock = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)];
sap.srcIP = GetNextHopIPfromDestinationIP(host_ip);
msg = sap.generateMessage();
def _sendto(*args, **kwargs):
	while True:
		try:
			sock[0].sendto(msg, (host_ip, host_port));
			time.sleep(2);	# Retry every 2 Second
			if not sock[0]:
				return;
			sys.stdout.write("Retrying . . .\n");
			sys.stdout.flush();
		except Exception as e:
			sys.stdout.write('ERROR: ' + str(e) + '\n');
			sys.stdout.flush();
thread_sendto = threading.Thread(target=_sendto);
thread_sendto.start();

# Receive Response
sys.stdout.write("Waiting for SAP Response\n");
sys.stdout.flush();
msg, sender = sock[0].recvfrom(4096); # Hope 4096 buffer size will be sufficient
while sender != (host_ip, host_port):
	msg, sender = sock[0].recvfrom(4096);
sock[0].close();
sock[0] = None;
sap = SAP.parseMessage(msg);
sdp = sap.get_Payload();
fw = open(argv[3], "w");
fw.write(sdp);
fw.close();

# End of SAP Client
sys.stdout.write("SAP Client Completed!\n");
sys.stdout.flush();

	

