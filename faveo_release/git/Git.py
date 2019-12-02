#!/usr/bin/env python

import subprocess


def log(data):
    print("[+] " + data)


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
        log("checking out to "+branch_name)
        self.execute("stash")
        self.execute("clean", "-fd")
        self.execute("checkout", branch_name, "-f")
        self.execute("fetch")
        self.execute("reset", "--hard", "origin/"+branch_name)
        log("checked out to "+branch_name)

    def sync_remote_branch_with_current_branch(self, remote_branch):
        log("force pushing current branch code to " + remote_branch)
        self.execute("push", "origin", "HEAD:" + remote_branch, "-f")
        log("force pushed current branch code to " + remote_branch)

    def commit_and_publish(self, branch):
        log("committing all changes")
        self.execute("add", ".")
        self.execute("commit", "-m", "product configuration updated", "-n")
        log("committed all changes")
        self.sync_remote_branch_with_current_branch(branch)

    def export(self, branch, path):
        absolute_path = path+'/'+branch+".zip"
        log('exporting source code to '+absolute_path)
        subprocess.call(['mkdir', '-p',  path])
        self.execute('archive', '--format', 'zip', '--output', absolute_path, branch)
        log('exported successfully')
