#!/usr/bin/python3
import os
from subprocess import run, Popen, PIPE, STDOUT


def execute(command):
    output = run(command,
                 stdout=PIPE,
                 stderr=PIPE,
                 cwd=os.getcwd(),
                 shell=True).stdout.decode('utf-8')

    return output


def execute_and_print(command):
    p = Popen(command,
              stdout=PIPE,
              stderr=STDOUT,
              cwd=os.getcwd(),
              shell=True)

    for line in iter(p.stdout.readline, ''):
        if not line:
            break

        print(line.decode("utf-8").rstrip())
