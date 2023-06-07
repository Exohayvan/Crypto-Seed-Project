import time
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from colorama import Fore, Style
import re
from collections import deque
import os, sys, time, platform, datetime
from bitcoinaddress import Wallet
import math

class AverageCounter:
    def __init__(self, intervals):
        self.intervals = intervals
        self.cycle_timestamps = deque()

    def add_cycle(self):
        current_time = time.time()
        self.cycle_timestamps.append(current_time)
        self._remove_old_cycles()

    def _remove_old_cycles(self):
        current_time = time.time()
        while self.cycle_timestamps and (current_time - self.cycle_timestamps[0] > max(self.intervals)):
            self.cycle_timestamps.popleft()

    def get_averages(self):
        current_time = time.time()
        averages = {}
        for interval in self.intervals:
            count = sum(1 for ts in self.cycle_timestamps if current_time - ts <= interval)
            average = count / (interval / 60)
            averages[interval] = math.floor(average)
        return averages

def random_proxy():
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pattern = re.compile(r'<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>')
        matches = pattern.findall(response.text)
        ip_address, port = random.choice(matches)
        time_print('Connecting to new proxy...')
        proxy = f"{ip_address}:{port}"
        time_print(Fore.BLUE + 'IP has changed to: ' + Fore.LIGHTYELLOW_EX + proxy + Fore.WHITE)
        return proxy
    else:
        print(f"Error: {response.status_code}")

def time_print(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = f"{Fore.BLUE}{Style.DIM}[{timestamp}]{Style.RESET_ALL}"
    print(timestamp, *args, **kwargs)

def mining(proxy):
    test = 'false'
    if proxy == 'true':
        test = 'true'
    counter = AverageCounter([1 * 60, 15 * 60, 30 * 60, 60 * 60])
    while True:
        if proxy == 0:
            time_print('Starting Address mining...')
            proxy = random_proxy()
            time.sleep(5)
            tbal = 0
            calls = 0
            count = 0
            index = 0
        else:
            wallet = Wallet()
            walletout = str(wallet)
            a, a, a, PrivateHex, a, a, a, PrivateWIF, a, a, a, a, PrivateWIFc, a, a, PublicKey, a, a, a, PublicKeyc, a, a, a, PublicAddress1, a, a, a, a, PublicAddress1c, a, a, a, PublicAddress3, a, a, a, a, PublicAddressbc1PKH, a, a, a, a, PublicAddressbc1WSH = walletout.split()
            addresses = [ PublicAddress1, PublicAddress1c, PublicAddress3, PublicAddressbc1PKH, PublicAddressbc1WSH]
            time_print(Fore.RED + 'Checking Private Key:' + Fore.WHITE + ' | ' + Style.DIM + PrivateHex)
            counter.add_cycle()
            averages = counter.get_averages()
            time_print(f"1-min average: {averages[1 * 60]}, 15-min average: {averages[15 * 60]}, 30-min average: {averages[30 * 60]}, 60-min average: {averages[60 * 60]}")
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = []
                for address in addresses:
                    results.append(executor.submit(check_balance, address, proxy, count))
            for index, future in enumerate(results):
                address = addresses[index]
                result = future.result()
                if result is not None:
                    if isinstance(result[1], float):
                        count += 1
                        calls += 1
                        time_print(f"#{count}: Address {result[0]} | {result[1]:.8f} BTC")

                    else:
                        print(f"#{index+1}: Address {result[0]} - {result[1]}")
            if tbal < 0:
                time_print(Fore.GREEN + 'BTC Found!')
            if calls > 249:
                proxy = random_proxy()
                calls = 0
        if test == 'true':
            print('Test Completed! Exiting in 5 seconds...')
                time.sleep(5)
                sys.exit()

def check_balance(address, proxy, count):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url, proxies={'http' : proxy})
        response.raise_for_status()
        data = response.json()
        balance = (data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]) / 100000000.0
        count += 0
        return (address, balance, count)
    except requests.exceptions.HTTPError as err:
        return (address, f"HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        return (address, f"Request error: {err}")
    except KeyError as err:
        return (address, f"Unexpected response format: {err}")
