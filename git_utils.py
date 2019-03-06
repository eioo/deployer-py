#!/usr/bin/python3
import sys
import process_utils


def get_git_repo_name(remote):
    output = process_utils.execute(f'git remote get-url {remote}')

    if not output:
        print('Not valid Git repo. Exiting')
        sys.exit()

    return output.strip().split('/')[-1].split('.git')[0]


def fetch_and_reset(remote, local):
    process_utils.execute('git fetch --all')
    process_utils.execute(f'git reset --hard {remote}/{local}')
