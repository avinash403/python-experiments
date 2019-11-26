#!/usr/bin/env python

import subprocess

faveo_base_path = "/var/www/html/faveo-helpdesk-advance/"

freelancer_branch = "freelancer-test"


def git(*args):
    dot_git_path = faveo_base_path + ".git"
    default_params = ["git", "--git-dir=" + dot_git_path]
    all_params = default_params + list(args)
    subprocess.call(all_params)

git('status')
