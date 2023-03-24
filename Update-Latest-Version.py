import requests
import os
import zipfile
import shutil

def update():
    # Set the GitHub repository and the version number to compare with
    repo_url = "https://api.github.com/repos/Exohayvan/Crypto-Seed-Project/releases/latest"
    version_number = "1.0"

    # Get the latest release information from the GitHub API
    response = requests.get(repo_url)
    data = response.json()

    # Extract the tag name from the response data
    latest_tag = data["tag_name"]

    # Compare the latest tag with the version number
    if latest_tag != version_number:
        # Download the latest release with "Build_Linux" in the name
        for asset in data["assets"]:
            if "Build_Linux" in asset["name"]:
                download_url = asset["browser_download_url"]
                download_response = requests.get(download_url)

                # Save the downloaded file to disk
                with open(asset["name"], "wb") as f:
                    f.write(download_response.content)

                # Extract the downloaded zip file
                with zipfile.ZipFile(asset["name"], "r") as zip_ref:
                    zip_ref.extractall()

                # Move all file contents to current script folder
                extracted_folder_name = asset["name"].replace(".zip", "")
                for root, dirs, files in os.walk(extracted_folder_name):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        dst_file_path = os.path.join(os.getcwd(), file)
                        shutil.move(src_file_path, dst_file_path)

                # Delete the extracted folder and the downloaded zip file
                shutil.rmtree(extracted_folder_name)
                os.remove(asset["name"])

                # Delete the script file
                os.remove(__file__)

                # Exit the script
                exit()

if __name__ == "__main__":
    update()
