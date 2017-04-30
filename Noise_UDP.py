from socket import *;
import time;
import sys;

MTU = 1492;
args = sys.argv;

# Get Port
try:
	port = int(args[1]);
	if port < 1024:
		port = 1024;
	elif port > 65535:
		port = 65535;
except:
	port = 65535;
	
# Get Size of Data
try:
	size = int(args[2]);
	if size < 0:
		size = 0;
	elif size > MTU - 52:
		size = MTU - 52;
except:
	size = MTU - 52;
	
# Get Interval / Delay
try:
	interval = float(args[3]);
	if interval < 1.0:
		interval = 1.0;
	elif interval > 1000.0:
		interval = 1000.0;
except:
	interval = 1000.0;

# Define Payload Size
payload = [];
for i in range (0, size):
	payload.append(chr(0xFF));
payload = ''.join(payload);
	
# Calculations & Printing
milli = int(interval);
micro = long(float(interval - int(interval)) * 1000);
sys.stdout.write("PAYLOAD " + str(size) + '\n');
sys.stdout.write("MILLI_SECS " + str(milli) + '\n');
sys.stdout.write("MICRO_SECS " + str(micro) + '\n');
sys.stdout.write("DATA_RATE " + str(((size + 52) * 8.0) / (float(milli) / 1000.0 + float(micro) / 1000000.0)) + '\n');
sys.stdout.flush();
# Process at Socket
sock = socket(AF_INET, SOCK_DGRAM); # UDP over IP
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1);
while True:
     sock.sendto(payload, ("255.255.255.255", port));
     time.sleep(interval / 1000.0);
