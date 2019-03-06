#!/usr/bin/python3
import argparse
import sys
from deployer import Deployer


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Deploy Node.js applications',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-s', '--script',
                        nargs='+',
                        help='Package.json script(s) to run', default='start')

    parser.add_argument('-c', '--npm-client',
                        choices=['npm', 'yarn'],
                        help='NPM client to use', default='npm')

    parser.add_argument('-lb', '--local-branch',
                        nargs='?',
                        help='Local branch name', default='master')

    parser.add_argument('-rb', '--remote-branch',
                        nargs='?',
                        help='Remote branch name', default='origin')

    parser.add_argument('-w', '--webhook-path',
                        nargs='?',
                        help='Path for Git webhook', default='/git/<reponame>/webhook')

    parser.add_argument('-p', '--webhook-port',
                        type=int, nargs='?',
                        help='Port for Git webhook', default=1337)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    try:
        d = Deployer(args)
    except KeyboardInterrupt:
        print('^C Exiting...')
        d.webhook.stop()
        sys.exit()
