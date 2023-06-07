import os, sys, time, platform, datetime #needed for system info
from colorama import Fore, Back, Style #needed for colored text
import http.client as httplib #needed for http requests
import requests, re #needed for http requests
from concurrent.futures import ThreadPoolExecutor #needed for multithreading
import zipfile, shutil #needed for extracting zip files
import argparse #needed for passing arguments
import json
import random
import hashlib, base64, ssl
from packages.proxy import random_proxy
from packages.update import update
from packages.coins.btc import mining as btc_mining

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
        "2": "Worker (Recommended)",
        "3": "Node (Experienced users only | Not Recommended)"
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

def compile():
    os_type = sys.platform.capitalize()
    if os_type == "Win32":
        os_type = "Windows"
    try:
        with open('data.json', 'r') as file:
            # Load the existing JSON data from file
            json_data = json.load(file)

            # Import the values from the JSON data
            version = json_data.get('version')
            address = json_data.get('address')
            is_node = json_data.get('is_node')
    except FileNotFoundError:
        print('data.json not found. Please run main.py first.')
        sys.exit()
    os.system('pip install pyinstaller')
    os.system(f'pyinstaller --onefile --exclude data.json --name {os_type}_Build-{version} main.py')
    folder_name = "build"

    folder_path = os.path.join(os.getcwd(), folder_name)

    # Use the os.rmdir() function to delete the folder
    shutil.rmtree(folder_path)
    print()
    print(f"Deleted {folder_path} folder")

    # Get the current working directory, where the script is located.
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # List all the files in the current directory.
    files = os.listdir(current_directory)

    # Iterate through the files.
    for file in files:
        # Check if the file has the '.spec' extension.
        if file.endswith(".spec"):
            # Construct the full path of the file.
            file_path = os.path.join(current_directory, file)
        
            # Delete the file.
            os.remove(file_path)
            print(f"Deleted {file_path}")
    # Get the current working directory (where your Python file is located)
    current_dir = os.getcwd()

    # Specify the source folder (dist)
    source_folder = os.path.join(current_dir, 'dist')

    # Check if the source folder exists
    if os.path.exists(source_folder):
        # Loop through all files in the source folder
        for file_name in os.listdir(source_folder):
            # Create the full file path
            file_path = os.path.join(source_folder, file_name)

            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                # Move the file to the current directory
                shutil.move(file_path, current_dir)

        # Delete the dist folder after moving all the files
        shutil.rmtree(source_folder)

        print("All files have been moved and the 'dist' folder has been deleted.")
    else:
        print("The specified source folder doesn't exist.")
    if os_type == "Linux":
        with open("run.sh", "w") as f:
            # write the script name to the file
            f.write(f'./{os_type}_Build-{version}.bin')
    sys.exit()

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
def checkInternetHttplib(url, timeout):
    time_print(Fore.WHITE + 'Checking Network Connection...')
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        response = connection.getresponse()
        if response.status == 200:
            time_print(Fore.GREEN + 'Connection to internet made.' + Fore.WHITE)
            return True
        elif response.status == 301:
            time_print(Fore.LIGHTRED_EX + 'Error 301: Moved Permanently or Server Problem.')
        elif response.status == 401:
            time_print(Fore.LIGHTRED_EX + 'Error 401: Unauthorized Access.')
        elif response.status == 402:
            time_print(Fore.LIGHTRED_EX + 'Error 402: Payment Required.')
        elif response.status == 404:
            time_print(Fore.LIGHTRED_EX + 'Error 404: Not Found.')
        elif response.status == 502:
            time_print(Fore.LIGHTRED_EX + 'Error 502: Bad Gateway. Server Problem.')
        else:
            time_print(Fore.LIGHTRED_EX + 'Error ' + str(response.status) + ': Connection Error')
        connection.close()
        sys.exit()
    except Exception as exep:
        time_print(exep)
        sys.exit(Fore.LIGHTRED_EX + 'Error, no internet connection')

def time_print(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = f"{Fore.BLUE}{Style.DIM}[{timestamp}]{Style.RESET_ALL}"
    print(timestamp, *args, **kwargs)
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
    print(f"User ID for address '{address}': {userID}")
    update(version, os_type)
    btc_mining(0)
    