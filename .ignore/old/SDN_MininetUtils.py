#!/usr/bin/python

import mininet.util;

from mininet.util import quietRun, moveIntf;

def _makeIntfPair( intf1, intf2, addr1=None, addr2=None, node1=None, node2=None,
                  deleteIntfs=True, runCmd=None ):
	"""Make a veth pair connnecting new interfaces intf1 and intf2
	   intf1: name for interface 1
	   intf2: name for interface 2
	   addr1: MAC address for interface 1 (optional)
	   addr2: MAC address for interface 2 (optional)
	   node1: home node for interface 1 (optional)
	   node2: home node for interface 2 (optional)
	   deleteIntfs: delete intfs before creating them
	   runCmd: function to run shell commands (quietRun)
	   raises Exception on failure

		Changes:
		The problem here is that we can not add a link to another
		netns within a Docker container since it does not know
		the other process (process not found error).
		So we have to do it different:
		We create the veth pair inside the default netns and move them
		into their netns (container) afterwards."""
		
	if deleteIntfs:
		# Delete any old interfaces with the same names
		quietRun( 'ip link del ' + intf1, shell=True )
		quietRun( 'ip link del ' + intf2, shell=True )

	# first: create the veth pair in default namespace
	if addr1 is None and addr2 is None:
		cmdOutput = quietRun( 'ip link add name %s '
							  'type veth peer name %s ' %
							  ( intf1, intf2 ),
							  shell=True )
	else:
		cmdOutput = quietRun( 'ip link add name %s '
							  'address %s '
							  'type veth peer name %s '
							  'address %s ' %
							  (  intf1, addr1, intf2, addr2 ),
							  shell=True )
	if cmdOutput:
		raise Exception( "Error creating interface pair (%s,%s): %s " %
						 ( intf1, intf2, cmdOutput ) )
	# second: move both endpoints into the corresponding namespaces
	moveIntf(intf1, node1)
	moveIntf(intf2, node2)

# Override Method
mininet.util.makeIntfPair = _makeIntfPair;