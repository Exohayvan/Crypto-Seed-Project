def w_update():
    # create or open the "updatetemp.txt" file in write mode
    with open(filename, "w") as f:
    # write the script name to the file
        f.write(version)
def r_update():
    if not os.path.exists('*.temp'):
        return
# Open the file "updatetemp.txt" in read mode
    with open(wildfilename, 'r') as file:
    # Read the contents of the file and store it in a variable
        old_version = file.read()
    cleanup(old_version)
def cleanup(old_version):
    time_print("Cleaning up old version files...")
    try:
        current_directory = os.getcwd()
        for root, dirs, files in os.walk(current_directory):
            for file in files:
                if old_version in file.lower():
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    time_print(f"Deleted: {file_path}")
    except Exception as e:
        time_print(f"Error while deleting files: {e}")
        time_print(f'Cleaned up old version: {old_version}')
def update(version):
    time_print('Checking for updates...')
    url = 'https://api.github.com/repos/exohayvan/Crypto-Seed-Project/releases'
    response = requests.get(url)
    release_data = response.json()

    latest_release = release_data[0]
    latest_tag = latest_release['tag_name']

    if latest_tag == version:
        time_print(f'Version is latest: {version}')
        r_update()
        return
    
    print()
    print(f'Current version is {version}, latest version is {latest_tag}')
    update = input("Would you like to update? (y/n)")

    if update == "y":
        # perform update
        time_print("Updating... Please wait... (This may take a while)")
        w_update()
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
                    print('System may ask for password to run the program. Please enter your password.')
                    os.system('sudo chmod +x run.sh')
                    os.system('sudo chmod +x *.bin')
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
