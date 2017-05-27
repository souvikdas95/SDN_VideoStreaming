__metaclass__ = type

import sys, time;

# Suppress .pyc generation
sys.dont_write_bytecode = True;

class SAP:
	"""
	# Author: Ramakrishna Mundugar, mundugar@nt.uni-saarland.de, Saarland University
	# Details: Implements RFC 2974 Session Announcement Protocol
	----------------------------SAP Packet Format------------------------------------
		0                   1                   2                   3
		0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
	   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	   | V=1 |A|R|T|E|C|   auth len    |         msg id hash           |
	   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	   |                                                               |
	   :                originating source (32 or 128 bits)            :
	   :                                                               :
	   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	   |                    optional authentication data               |
	   :                              ....                             :
	   *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	   |                      optional payload type                    |
	   +                                         +-+- - - - - - - - - -+
	   |                                         |0|                   |
	   + - - - - - - - - - - - - - - - - - - - - +-+                   |
	   |                                                               |
	   :                            payload                            :
	   |                                                               |
	   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	----------------------------SAP Packet Format------------------------------------
	"""
	def __init__(self):
		""" 
		Initializes SAP protocol class
		"""
		self.v = str(1);
		self.srcIP = '';
		self.msgID = '';
		self.Payload = '';
	
	def set_srcIP(self, srcIP):
		self.srcIP = srcIP;
			
	def set_Payload(self, Payload):
		self.Payload = Payload;
		
	def get_v(self):
		return self.v;
		
	def get_srcIP(self):
		return self.srcIP;
		
	def get_msgID(self):
		return self.msgID;
		
	def get_Payload(self):
		return self.Payload;
		
	def generateMessage(self, msgID = None):
		if msgID:
			self.msgID = msgID;
		else:
			self.msgID = str(int(time.time()));
		msg = "v" + "=" + self.v + ",";
		msg = msg + "srcIP" + "=" + self.srcIP + ",";
		msg = msg + "msgID" + "=" + self.msgID + "$";
		msg = msg + self.Payload;
		return msg;

	@staticmethod
	def parseMessage(msg):
		ret = SAP();
		msg, ret.Payload = msg.split('$');
		for line in msg.split(','):
			name, value = line.split('=');
			if name == "v":
				if int(value) != 1:
					print("SAP Version ERROR");
					return None;
				ret.v = value;
			elif name == "srcIP":
				ret.srcIP = value;
			elif name == "msgID":
				ret.msgID = value;
		return ret;
		
		
	
