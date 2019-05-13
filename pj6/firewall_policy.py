#!/usr/bin/python
# CS 6250 Spring 2019 - Project 6 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def make_firewall_policy(config):


    rules = []

    for entry in config:

        rule = match()
        if entry['macaddr_src'] != '-':
            rule &= match(srcmac = EthAddr(entry['macaddr_src']), ethtype = packet.IPV4)
        if entry['ipaddr_src'] != '-' :
            rule &= match(srcip = IPAddr(entry['ipaddr_src']), ethtype = packet.IPV4)
        if entry['macaddr_dst'] != '-' :
            rule &= match(dstmac = EthAddr(entry['macaddr_dst']), ethtype = packet.IPV4)
        if entry['ipaddr_dst'] != '-' :
            rule &= match(dstip = IPAddr(entry['ipaddr_dst']), ethtype = packet.IPV4)
        if entry['port_src'] != '-' :
            rule &= match(scrport = int(entry['port_scr']), ethtype = packet.IPV4)

        if entry['port_dst'] != '-':
            rule &= match(dstport = int(entry['port_dst']), ethtype = packet.IPV4)
        if entry['protocol'] == 'T':
            rule &= match(protocol = packet.TCP_PROTO, ethtype = packet.IPV4)
        if entry['protocol'] == 'U':
            rule &= match(protocol = packet.UDP_PROTO, ethtype = packet.IPV4)
        if entry['protocol'] == 'I':
            rule &= match(protocol = packet.ICMP_PROTO, ethtype = packet.IPV4)
        if entry['protocol'] == 'B':
            rule1 = rule & match(protocol = packet.UDP_PROTO, ethtype = packet.IPV4)
            rules.append(rule1)
            rule &= match(protocol = packet.TCP_PROTO, ethtype = packet.IPV4)


        rules.append(rule)
        pass


    allowed = ~(union(rules))

    return allowed
