import os, sys, time, platform, datetime #needed for system info
from colorama import Fore, Back, Style #needed for colored text
import http.client as httplib #needed for http requests
import requests, re #needed for http requests
from concurrent.futures import ThreadPoolExecutor #needed for multithreading
import zipfile, shutil #needed for extracting zip files
import argparse #needed for passing arguments
import json
import random
import asyncio
import httpx
import hashlib, base64, ssl
from packages.proxy import random_proxy
from packages.update import update
from packages.coins.btc import mining as btc_mining
from packages.time_print import time_print
from packages.compile import compile
from packages.checkhttp import checkInternetHttplib
import nest_asyncio
nest_asyncio.apply()

msg = "Project for brute forcing private keys, using parallel processing across a network of everyone running the program! For educational use only."
parser = argparse.ArgumentParser(description = msg)

parser.add_argument("-t", "--test", help = "Test script. Values: 'true'")
parser.add_argument("-c", "--compile", help = "Compile script for system. Values: 'onefile' 'ipa'")
parser.add_argument("-v", "--version", help = "Check Versions. Values: 'true'")
args = parser.parse_args()

#setting const
version = 'v0.0.9-alpha'
filename = 'update.temp'
os_type = sys.platform
filename = version +'_update.temp'
wildfilename = '*_update.temp'
if os_type == 'win32':
    os_type = 'windows'
    from colorama import just_fix_windows_console
    just_fix_windows_console()

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
    supported_os_types = ['linux', 'windows']
    if os_type in supported_os_types:
        time_print(Fore.GREEN + f'Valid system type. {os_type.capitalize()} detected.' + Fore.WHITE)
    else:
        time_print(Fore.LIGHTRED_EX + 'Unknown system type. Please reach out to support, even if program seems to work. We want to try and add support for all systems we can. Please send us this info ' + Fore.YELLOW +'"platform: ' + os_type + '" ' + '"machine: ' + platform.machine() + '"'+ Fore.WHITE)

def ask_run():
    choices = {
        "1": "Solo (Not Recommended)",
        "2": "Worker (Recommended) THIS IS NOT WORKING RIGHT NOW!",
        "3": "Node (Experienced users only | Not Recommended) THIS IS NOT WORKING RIGHT NOW!"
    }

    config_file = 'config.json'

    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
            if 'run_mode' in data:
                print("The value already exists in the config file. Skipping user input.")
                return

    print("How would you like to run this program?")
    print("(If unsure choose 'Worker')")
    for key, value in choices.items():
        print(f"{key}) {value}")
    
    user_choice = input("Enter your choice (1, 2, or 3): ")

    while user_choice not in choices:
        print("Invalid choice. Please choose either 1, 2, or 3.")
        user_choice = input("Enter your choice (1, 2, or 3): ")

    choice_data = {"run_mode": choices[user_choice]}

    with open(config_file, 'w') as f:
        json.dump(choice_data, f)

    print("Your choice has been saved to config.json.")

def generate_id(address, id_length=12):
    # Create SHA-512 hash object
    hasher = hashlib.sha512()

    # Update the hash object with the address bytes
    hasher.update(address.encode('utf-8'))

    # Get the binary representation of the hash
    binary_hash = hasher.digest()

    # Encode the binary hash using base64
    base64_hash = base64.b64encode(binary_hash).decode('utf-8')

    # Remove any non-alphanumeric characters and truncate to the desired length
    alphanumeric_hash = ''.join(c for c in base64_hash if c.isalnum())
    short_id = alphanumeric_hash[:id_length]

    return short_id

def is_valid_btc_address(address):
    pattern = '^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$'
    return re.match(pattern, address) is not None

def data_json():
    # Check if the JSON file exists
    try:
        with open('data.json', 'r') as file:
            # Load the existing JSON data from file
            json_data = json.load(file)

            # Import the values from the JSON data
            jversion = json_data.get('version')
            address = json_data.get('address')
            is_node = json_data.get('is_node')
    except FileNotFoundError:
        # If the JSON file does not exist, use version as jversion
        jversion = version

        # Ask the user for input for address and check if it is a valid BTC address
        while True:
            address = input('Please enter a BTC address: ')
            if is_valid_btc_address(address):
                break
            else:
                print('Invalid BTC address. Please try again.')

        # Set is_node to False
        is_node = False

        # Create a dictionary with the new data
        data = {
            "version": jversion,
            "address": address,
            "is_node": is_node
        }

        # Save the new data to the JSON file
        with open('data.json', 'w') as file:
            json.dump(data, file)
    else:
        # If the JSON file exists, check if jversion matches version
        if jversion != version:
            # If they do not match, update the JSON file with the new version
            json_data['version'] = version
            with open('data.json', 'w') as file:
                json.dump(json_data, file)

    # Generate the userID based on the address
    userID = generate_id(address)

    # Return the imported or entered values, along with the generated userID
    return jversion, address, is_node, userID

# Call the data_json function to retrieve the values
    
#main functions
#runtime order

if args.test == 'true':
    checkInternetHttplib("www.google.com", 3)
    print('Testing Mode...')
    time_print(Fore.LIGHTRED_EX + Fore.YELLOW +'"platform: ' + os_type + '" ' + '"machine: ' + platform.machine() + '"'+ Fore.WHITE)
    btc_mining(args.test)
elif args.compile == 'onefile':
    print('Compiling File')
    compile()
elif args.compile == 'ipa':
    print('not ready!')
    sys.exit()
elif args.version == 'true':
    print(version)
else:
    ask_run()
    checkInternetHttplib("www.google.com", 3)
    intro()
    jversion, address, is_node, userID = data_json()
    print(f"{Fore.LIGHTCYAN_EX}User ID: {userID}")
    update(version, os_type)
    asyncio.run(btc_mining(0))
    