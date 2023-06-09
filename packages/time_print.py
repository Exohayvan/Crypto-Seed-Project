import os, sys, time, platform, datetime
from colorama import Fore, Back, Style

def time_print(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = f"{Fore.BLUE}{Style.DIM}[{timestamp}]{Style.RESET_ALL}"
    print(timestamp, *args, **kwargs)
