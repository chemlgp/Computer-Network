#!/usr/bin/python
# CS6250 Computer Networks Project 1
# Creates a datacenter topology based on command line parameters and starts the Mininet Command Line Interface.

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output, setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import argparse
import sys
import os

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Datacenter Topologies")

parser.add_argument('--fi',
                    type=int,
                    help=("Number of Fan-in Switches to create."
                    "Must be >= 1"),
                    required=True)

parser.add_argument('--n',
                    type=int,
                    help=("Number of hosts to create in each lower level switch."
                    "Must be >= 1"),
                    required=True)

args = parser.parse_args()

lg.setLogLevel('info')

# Topology to be instantiated in Mininet
class DataCenter(Topo):
    "DataCenter Topology"

    def __init__(self, n=1, delay='0ms', fi=1,  cpu=.01, max_queue_size=None, **params):
        """Star Topology with fi fan-in  zones.
           n: number of hosts per low level switch
           cpu: system fraction for each host
           bw: link bandwidth in Mb/s
           delay: link latency (e.g. 10ms)"""
        self.cpu = 1 / ((n * fi * fi) * 1.5)

        # Initialize topo
        Topo.__init__(self, **params)

        hostConfig = {'cpu': cpu}
        #NOTE:  Switch to Switch links will be bw=10 delay=0
        #NOTE:  Hosts to Switch links will be bw=1 delay=1
        #NOTE:  Use the following configurations as appropriate when creating the links
	swlinkConfig = {'bw': 10, 'delay': '0ms', 'max_queue_size': max_queue_size}
        hostlinkConfig = {'bw': 1, 'delay': '1ms','max_queue_size': max_queue_size}
        tls = self.addSwitch('tls1')

        for i in range(1,fi+1):
            tempstrnum = str(i)
            name = "mls" + tempstrnum
            locals()["mls{}".format(i)] = self.addSwitch(name)
            self.addLink(tls,locals()["mls{}".format(i)],**swlinkConfig)
            for j in range(1,fi+1):
                tempstrnum_s = str(j)
                name_ss = "s" + tempstrnum + "x" + tempstrnum_s
                locals()["s{}x{}".format(i,j)] = self.addSwitch(name_ss)
                self.addLink(locals()["mls{}".format(i)],locals()["s{}x{}".format(i,j)],**swlinkConfig)
                for k in range(1,n+1):
                    name_host = "h"+tempstrnum +"x" +tempstrnum_s + "x"+ str(k)
                    locals()["h{}x{}x{}".format(i,j,k)]= self.addHost(name_host,**hostConfig)
                    self.addLink(locals()["h{}x{}x{}".format(i,j,k)],locals()["s{}x{}".format(i,j)],**hostlinkConfig)








def main():
    "Create specified topology and launch the command line interface"
    topo = DataCenter(n=args.n, fi=args.fi)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
