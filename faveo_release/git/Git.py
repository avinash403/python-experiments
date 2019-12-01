#!/usr/bin/env python

import subprocess


class Git:
    def __init__(self, base_path, log_path = './faveo_release.log'):
        self.basePath = base_path
        self.logPath = log_path

    def execute(self, *args):
        """
        Performs git operations based on the params passed
        :param args:
        :return:
        """
        default_params = ["git", "-C", self.basePath]
        all_params = default_params + list(args)
        subprocess.call(all_params, stdout=open(self.logPath, 'a'), stderr=open(self.logPath, 'a'))

    def checkout(self, branch_name):
        self.execute("stash")
        self.execute("clean", "-fd")
        self.execute("checkout", branch_name, "-f")
        self.execute("fetch")
        self.execute("reset", "--hard", "origin/"+branch_name)
