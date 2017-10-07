import sys;
import time;

from socket import *;
from struct import pack;
from struct import unpack;

# IP-INT conversion methods
IP2INT = lambda ipstr: unpack('!I', inet_aton(ipstr))[0]; 	# IP Address to Integer
INT2IP = lambda n: inet_ntoa(pack('!I', n));              	# Integer to IP Address

MTU = 1492;
args = sys.argv;
cur_arg = 1;

# Get Noise Type
try:
	noise_type = int(args[cur_arg]);
	if noise_type < 1:
		noise_type = 1;
	elif noise_type > 2:
		noise_type = 2;
except:
	noise_type = 1;
cur_arg += 1;

# Get Destination Address
if noise_type == 2:
	try:
		destination_address = IP2INT(args[cur_arg]);
	except:
		sys.stdout.write("\n*** Warning: Invalid Destination Address. Switching to Broadcast Noise.\n");
		sys.stdout.flush();
		noise_type = 1;
	cur_arg += 1;

# Get Destination Port
try:
	destination_port = int(args[cur_arg]);
	if destination_port < 1024:
		destination_port = 1024;
	elif destination_port > 65535:
		destination_port = 65535;
except:
	destination_port = 65535;
cur_arg += 1;

# Get Size of Data
try:
	size = int(args[cur_arg]);
	if size < 0:
		size = 0;
	elif size > MTU - 52:
		size = MTU - 52;
except:
	size = MTU - 52;
cur_arg += 1;
	
# Get Interval / Delay
try:
	interval = float(args[cur_arg]);
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
if noise_type == 1:
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1);
	while True:
	     sock.sendto(payload, ("255.255.255.255", destination_port));
	     time.sleep(interval / 1000.0);
elif noise_type == 2:
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 0);
	while True:
	     sock.sendto(payload, (INT2IP(destination_address), destination_port));
	     time.sleep(interval / 1000.0);