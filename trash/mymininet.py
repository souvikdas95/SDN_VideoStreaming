#!/usr/bin/python

"""
Documentation Pending
"""

import sys

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Node
from mininet.util import waitListening
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import OVSLink
from mininet.link import OVSIntf
from mininet.clean import Cleanup

NOISE_SWITCHES = 100;
NOISE_HOSTS_PER_SWITCH = 10;

if __name__ == '__main__':
    setLogLevel('info');

    net = Mininet(topo = None, controller = None, build = False);

    info('*** Connecting to controller\n');
    net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6653);

    info('*** Creating switches (Open vSwitch w/ OpenFlow13)\n');
    s1 = net.addSwitch('s1', cls = OVSSwitch, protocols = 'OpenFlow13', inband = True, stp = True);
    s2 = net.addSwitch('s2', cls = OVSSwitch, protocols = 'OpenFlow13', inband = True, stp = True);
    s3 = net.addSwitch('s3', cls = OVSSwitch, protocols = 'OpenFlow13', inband = True, stp = True);
    s4 = net.addSwitch('s4', cls = OVSSwitch, protocols = 'OpenFlow13', inband = True, stp = True);
    s5 = net.addSwitch('s5', cls = OVSSwitch, protocols = 'OpenFlow13', inband = True, stp = True);

    info('*** Establishing Switch Mesh\n');
    cSw = len(net.switches);
    for i in range(cSw - 1):
        for j in range(i + 1, cSw):
            net.addLink(net.switches[i], net.switches[j]);

    info('*** Creating hosts\n');
    h1 = net.addHost('h1', ip = '10.0.0.128');
    h2 = net.addHost('h2', ip = '10.0.0.129');
    h3 = net.addHost('h3', ip = '10.0.0.130');
    h4 = net.addHost('h4', ip = '10.0.0.131');
    h5 = net.addHost('h5', ip = '10.0.0.132');
    h6 = net.addHost('h6', ip = '10.0.0.133');
    h7 = net.addHost('h7', ip = '10.0.0.134');
    h8 = net.addHost('h8', ip = '10.0.0.135');
    h9 = net.addHost('h9', ip = '10.0.0.136');
    h10 = net.addHost('h10', ip = '10.0.0.137');

    info('*** Creating Host-Switch Links\n');
    net.addLink(s1, h1);
    net.addLink(s1, h2);
    net.addLink(s2, h3);
    net.addLink(s2, h4);
    net.addLink(s3, h5);
    net.addLink(s3, h6);
    net.addLink(s4, h7);
    net.addLink(s4, h8);
    net.addLink(s5, h9);
    net.addLink(s5, h10);

    #info('*** Enable NAT\n');
    #net.addNAT(connect = s1);

    info('*** Starting Network\n');
    net.start();

    info('*** Configure Host Default Routes\n');
    #h1.cmd('route add default gw 10.0.0.128 eth-h1');
    #h2.cmd('route add default gw 10.0.0.129 eth-h2');
    #h3.cmd('route add default gw 10.0.0.130 eth-h3');
    #h4.cmd('route add default gw 10.0.0.131 eth-h4');
    #h5.cmd('route add default gw 10.0.0.132 eth-h5');
    #h6.cmd('route add default gw 10.0.0.133 eth-h6');
    #h7.cmd('route add default gw 10.0.0.134 eth-h7');
    #h8.cmd('route add default gw 10.0.0.135 eth-h8');
    #h9.cmd('route add default gw 10.0.0.136 eth-h9');
    #h10.cmd('route add default gw 10.0.0.137 eth-h10');
    h1.setDefaultRoute(h1.defaultIntf());
    h2.setDefaultRoute(h2.defaultIntf());
    h3.setDefaultRoute(h3.defaultIntf());
    h4.setDefaultRoute(h4.defaultIntf());
    h5.setDefaultRoute(h5.defaultIntf());
    h6.setDefaultRoute(h6.defaultIntf());
    h7.setDefaultRoute(h7.defaultIntf());
    h8.setDefaultRoute(h8.defaultIntf());
    h9.setDefaultRoute(h9.defaultIntf());
    h10.setDefaultRoute(h10.defaultIntf());

    info('*** Configure Host Interfaces\n');
    #h1.cmd('ethtool -s h1-eth0 speed 1 duplex full autoneg off');
    #h2.cmd('ethtool -s h2-eth0 speed 1 duplex full autoneg off');
    #h3.cmd('ethtool -s h3-eth0 speed 1 duplex full autoneg off');
    #h4.cmd('ethtool -s h4-eth0 speed 1 duplex full autoneg off');
    #h5.cmd('ethtool -s h5-eth0 speed 1 duplex full autoneg off');
    #h6.cmd('ethtool -s h6-eth0 speed 1 duplex full autoneg off');
    #h7.cmd('ethtool -s h7-eth0 speed 1 duplex full autoneg off');
    #h8.cmd('ethtool -s h8-eth0 speed 1 duplex full autoneg off');
    #h9.cmd('ethtool -s h9-eth0 speed 1 duplex full autoneg off');
    #h10.cmd('ethtool -s h10-eth0 speed 1 duplex full autoneg off');

    info('*** Configure switches (Open vSwitch w/ OpenFlow13)\n');
    #s1.cmd('ifconfig s1 10.0.0.64');
    #s2.cmd('ifconfig s2 10.0.0.65');
    #s3.cmd('ifconfig s3 10.0.0.66');
    #s4.cmd('ifconfig s4 10.0.0.67');
    #s5.cmd('ifconfig s5 10.0.0.68');
    #s1.cmd('ethtool -s s1 speed 1 duplex full autoneg off');
    #s2.cmd('ethtool -s s2 speed 1 duplex full autoneg off');
    #s3.cmd('ethtool -s s3 speed 1 duplex full autoneg off');
    #s4.cmd('ethtool -s s4 speed 1 duplex full autoneg off');
    #s5.cmd('ethtool -s s5 speed 1 duplex full autoneg off');
    #s1.cmd('ovs-vsctl set bridge s1 stp-enable=true rstp-enable=true');
    #s2.cmd('ovs-vsctl set bridge s2 stp-enable=true rstp-enable=true');
    #s3.cmd('ovs-vsctl set bridge s3 stp-enable=true rstp-enable=true');
    #s4.cmd('ovs-vsctl set bridge s4 stp-enable=true rstp-enable=true');
    #s5.cmd('ovs-vsctl set bridge s5 stp-enable=true rstp-enable=true');

    info('*** Switching to CLI\n');
    #CLI(net);

    info('*** Stopping Network\n');
    net.stop();

    info('*** Cleaning Up\n');
    Cleanup.cleanup();
