#!/usr/bin/env python

import scapy.all as scapy
import prettytable


def scan(ip):
    # scapy_all.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="11:11:11:11:11:11")
    arp_request_broadcast = broadcast/arp_request
    # (answered_list, unanswered_list) = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]

    client_list = []
    for element in answered_list:
        # element is tuple of sent and answered. We need only answered
        # print(element[1].show())
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
        # print(element[1].psrc+"\t\t\t" + element[1].hwsrc)
        # print(element[1].hwsrc)

    return client_list

    # print(arp_request.summary(), broadcast.summary())
    # print(arp_request.show(), broadcast.show())
    # print(arp_request_broadcast.show())
    # scapy.ls(scapy.Ether())


def print_result(result_list):
    table = prettytable.PrettyTable(["Ip", "Mac Address"])
    for element in result_list:
        table.add_row([element['ip'], element['mac']])
    print(table)


print_result(scan("192.168.2.1/24"))
