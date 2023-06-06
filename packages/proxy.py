import requests
import random
import re
    
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
