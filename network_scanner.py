#!/usr/bin/env python

import scapy.all as scapy
import prettytable
import optparse


def scan(ip):
    # scapy_all.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="11:11:11:11:11:11")
    arp_request_broadcast = broadcast / arp_request
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


def get_target():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="range of IP addresses")
    options = parser.parse_args()[0]
    if not options.target:
        parser.error("Please specify an IP range")
    return options.target


print_result(scan(get_target()))
