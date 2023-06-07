import sys
import os
import json
import shutil

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
