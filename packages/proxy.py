import requests
import random
import re
import datetime
import aiohttp
import asyncio
from colorama import Fore, Back, Style
from .time_print import time_print

async def is_proxy_working(proxy):
    """
    Asynchronously check if a proxy is working by attempting to access Google's homepage.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://www.google.com/', proxy=proxy, timeout=5) as response:
                if response.status == 200:
                    return True
        except:
            return False

async def check_proxies(proxies):
    """
    Asynchronously check a list of proxies.
    """
    tasks = [is_proxy_working(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    working_proxies = [proxy for proxy, works in zip(proxies, results) if works]
    return working_proxies

def random_proxy():
    """
    Fetch a list of proxies and return a random one that's operational.
    """
    time_print(Fore.YELLOW + 'Connecting to new proxy...')
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pattern = re.compile(r'<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>')
        matches = pattern.findall(response.text)
        
        proxies = [f"http://{ip_address}:{port}" for ip_address, port in matches]

        # Check proxies concurrently
        loop = asyncio.get_event_loop()
        working_proxies = loop.run_until_complete(check_proxies(proxies))

        if working_proxies:
            chosen_proxy = random.choice(working_proxies)
            time_print(Fore.GREEN + 'Connected to new proxy!')
            time_print(Fore.BLUE + 'IP has changed to: ' + Fore.LIGHTYELLOW_EX + chosen_proxy + Fore.WHITE)
            return chosen_proxy
        else:
            time_print(Fore.RED + 'No working proxies found.' + Fore.WHITE)
    else:
        print(f"Error: {response.status_code}")