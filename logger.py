#!/usr/bin/python3
import time

from colorama import Fore


def log(message):
    print(f"[{Fore.CYAN + time.strftime('%H:%M:%S', time.localtime())}]{Fore.RESET + message}")
