import os, sys, time, platform, datetime #needed for system info
from colorama import Fore, Back, Style #needed for colored text
import http.client as httplib #needed for http requests
import requests, json #needed for http requests
from concurrent.futures import ThreadPoolExecutor #needed for multithreading
import zipfile, shutil #needed for extracting zip files

#setting const
version = 'v0.0.3-alpha'
filename = 'update.temp'
os_type = sys.platform

#startup functions
def intro():
    columns = os.get_terminal_size().columns
    if os_type == 'linux':
        os.system('clear')
    if os_type == 'windows':
        os.system('cls')
    string = str(Fore.BLUE + 'Crypto Seed Project')
    print(string.center(columns))
    string = str(Fore.BLUE + 'Programmed with' + Fore.RED + ' <3')
    print(string.center(columns))
    string = str(Fore.BLUE + 'Made by ExoHayvan')
    print(string.center(columns))
    time_print(Fore.WHITE + 'Starting...')
    time_print('Checking System Type...')
    if os_type == 'linux':
        time_print(Fore.GREEN + 'Valid system type. Lunix detected.' + Fore.WHITE)
    elif os_type == 'windows':
        time_print(Fore.GREEN + 'Valid system type. Windows detected.' + Fore.WHITE)
    else:
        time_print(Fore.LIGHTRED_EX + 'Unknown system type. Please reach out to support, even if program seems to work. We want to try and add support for all systems we can. Please send us this info ' + Fore.YELLOW +'"platform: ' + os_type + '" ' + '"machine: ' + platform.machine() + '"'+ Fore.WHITE)

#update functions
def w_update():
    # create or open the "updatetemp.txt" file in write mode
    with open(filename, "w") as f:
    # write the script name to the file
        f.write(version)
def r_update():
# Open the file "updatetemp.txt" in read mode
    with open(filename, 'r') as file:
    # Read the contents of the file and store it in a variable
        old_version = file.read()
    cleanup(old_version)
def cleanup(old_version):

# get the current working directory
    cwd = os.getcwd()

# get the full path of the file
    file_path = os.path.join(cwd, filename)

# delete the file
    os.remove(file_path)
def update(version):
    time_print('Checking for updates...')
    url = 'https://api.github.com/repos/exohayvan/Crypto-Seed-Project/releases'
    response = requests.get(url)
    release_data = response.json()

    latest_release = release_data[0]
    latest_tag = latest_release['tag_name']

    if latest_tag == version:
        time_print(f'Already on the latest version {version}')
        return
    
    print()
    print(f'Current version is {version}, latest version is {latest_tag}')
    update = input("Would you like to update? (y/n)")

    if update == "y":
        # perform update
        time_print("Updating... Please wait... (This may take a while)")
        if os_type == 'windows':
            asset_name = 'Windows_Build'
        if os_type == 'linux':
            asset_name = 'Linux_Build'
        else:
            print("Update Required...")
            print(f'Auto updates not made for build. Please download from {url}')
            sys.exit()

        for asset in latest_release['assets']:
            if asset_name in asset['name']:
                download_url = asset['browser_download_url']
                time_print(f'Downloading {download_url}')
                download_response = requests.get(download_url)
                with open(asset['name'], 'wb') as f:
                    f.write(download_response.content)
                with zipfile.ZipFile(asset['name'], 'r') as zip_ref:
                    zip_ref.extractall('.')
                    time_print(f'Unzipping {asset["name"]}')
                os.remove(asset['name'])
                time_print(f'Updated to version {latest_tag}')
                time_print("Reloading...")
                if os_type == 'linux':
                    os.system('./run.sh')
                if os_type == 'windows':
                    os.system(f'start *{latest_tag}.exe')
                sys.exit()
        else:
            time_print(f'Error: No {asset_name} build found in release {latest_tag}')
            time_print("Exiting in 5 seconds...")
            time.sleep(5)
            sys.exit()
    else:
        # print message and wait before exiting
        time_print("Update is required. Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit()
       
#main functions
def checkInternetHttplib(url, timeout):
    time_print(Fore.WHITE + 'Checking Network Connection...')
    connection = httplib.HTTPConnection(url,
                                        timeout=timeout)
    try:
        connection.request("HEAD","/")
        connection.close()
        time_print(Fore.GREEN + 'Connection to internet made.' + Fore.WHITE)
        return True
    except Exception as exep:
        time_print(exep)
        sys.exit(Fore.LIGHTRED_EX + 'Error, no internet connection')
def mining(proxy):
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

#status/misc functions       
def discord(title, message, color, field1, value1, field2, value2, field3, value3):
    from discordwebhook import Discord
    webhook_url = 'https://discord.com/api/webhooks/1076028464802570281/Pvq3XXe2WvZF-0PLQpCWtZ38AgRSJgP-6KyjL5R2lRV9Prff7r0SogtVJ_arvpLKiDHW'
    discord = Discord(url=webhook_url)
    discord.post(
        embeds=[
            {
                "title": title,
                "description": message,
                "color": color,
                "fields": [
                    {"name": field1, "value": value1, "inline": True},
                    {"name": field2, "value": value2, "inline": True},
                    {"name": field3, "value": value3},
                ],
            }
        ],
    )
def time_print(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = f"{Fore.BLUE}{Style.DIM}[{timestamp}]{Style.RESET_ALL}"
    print(timestamp, *args, **kwargs)
def random_proxy():
    import requests
    import random
    import re
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
        time_print(Fore.BLUE + 'IP has changed to: ' + Fore.LIGHTYELLOW_EX+ proxy)
        return proxy
    else:
        print(f"Error: {response.status_code}")

#runtime order
intro()
checkInternetHttplib("www.google.com", 3)
update(version)
#discord('BTC Seed Mining Network Stats', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0xf7931a, 'Nodes Online:', 'N/A', 'Round:', 'N/A', 'Shares:', 'N/A')
from bitcoinaddress import Wallet
mining(0)
