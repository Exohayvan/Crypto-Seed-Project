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
from colorama import Fore, Back, Style
import httpx
import asyncio
from ..proxy import random_proxy
from ..time_print import time_print

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

async def check_balance(address, proxy, count):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        async with httpx.AsyncClient(proxies={"http://*": proxy}) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            balance = (data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]) / 100000000.0
            return (address, balance, count)
    except httpx.HTTPStatusError as err:
        return (address, f"HTTP error: {err}")
    except httpx.RequestError as err:
        return (address, f"Request error: {err}")
    except KeyError as err:
        return (address, f"Unexpected response format: {err}")

async def mining(proxy):
    test = 'false'
    count = 0
    num_cores = os.cpu_count() or 1
    max_workers = 50 * num_cores
    
    if proxy == 'true':
        test = 'true'
        proxy = 0
    counter = AverageCounter([1 * 60, 15 * 60, 30 * 60, 60 * 60])
    
    while True:
        if proxy == 0:
            time_print(f'Starting Address mining with {Fore.MAGENTA}{max_workers} workers...{Fore.RESET}')
            proxy = f"http://{random_proxy()}"
            time.sleep(5)
            tbal = 0
            calls = 0
            index = 0
        else:
            wallet = Wallet()
            walletout = str(wallet)
            a, a, a, PrivateHex, a, a, a, PrivateWIF, a, a, a, a, PrivateWIFc, a, a, PublicKey, a, a, a, PublicKeyc, a, a, a, PublicAddress1, a, a, a, a, PublicAddress1c, a, a, a, PublicAddress3, a, a, a, a, PublicAddressbc1PKH, a, a, a, a, PublicAddressbc1WSH = walletout.split()
            addresses = [PublicAddress1, PublicAddress1c, PublicAddress3, PublicAddressbc1PKH, PublicAddressbc1WSH]
            time_print(Fore.RED + 'Checking Private Key:' + Fore.WHITE + ' | ' + Style.DIM + PrivateHex)
            
            counter.add_cycle()
            averages = counter.get_averages()
            time_print(f"{Fore.BLUE}Average {Fore.WHITE}| {Fore.BLUE}1-min: {averages[1 * 60]} {Fore.WHITE}| {Fore.BLUE}15-min: {averages[15 * 60]} {Fore.WHITE}| {Fore.BLUE}30-min: {averages[30 * 60]} {Fore.WHITE}| {Fore.BLUE}60-min: {averages[60 * 60]}")
            
            tasks = [check_balance(address, proxy, count) for address in addresses]
            results = await asyncio.gather(*tasks)

            for index, result in enumerate(results):
                address = addresses[index]
                if result is not None:
                    if isinstance(result[1], float):
                        count += 1
                        calls += 1
                        time_print(f"#{count}: Address {result[0]} | {result[1]:.8f} BTC")
                    else:
                        print(f"#{index+1}: Address {result[0]} - {result[1]}")
            
            if tbal < 0:
                time_print(Fore.GREEN + 'BTC Found!')
                print("Press 'ENTER' key to continue...")
                input()
            
            if calls > 249:
                proxy = random_proxy()
                calls = 0

        if test == 'true':
            print('Test Completed! Exiting in 5 seconds...')
            await asyncio.sleep(5)
            sys.exit()