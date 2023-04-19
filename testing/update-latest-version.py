import requests
import os
import zipfile
import shutil

def update():
    # Set the GitHub repository and the version number to compare with
    owner = "exohayvan"
    repo = "Crypto-Seed-Project"
    version_number = "1.0"

    # Construct the URL to retrieve all releases for the repository
    releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    # Send a GET request to retrieve the releases
    response = requests.get(releases_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Get the latest release information
        latest_release = data[0]

        # Extract the tag name from the latest release data
        latest_tag = latest_release["tag_name"]

        # Compare the latest tag with the version number
        if latest_tag != version_number:
            # Download the latest release with "Build_Linux" in the name
            for asset in latest_release["assets"]:
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

                            # Extract the body of the latest release and save it to update-notes.txt
                            if file == "RELEASE_NOTES.md":
                                with open("update-notes.txt", "w") as notes_file:
                                    with open(dst_file_path, "r") as release_file:
                                        release_body = release_file.read()
                                        notes_file.write(release_body)

                    # Delete the extracted folder and the downloaded zip file
                    shutil.rmtree(extracted_folder_name)
                    os.remove(asset["name"])

                    # Delete the script file
                    os.remove(__file__)

                    # Exit the script
                    exit()

    else:
        # Print an error message if the request was not successful
        print(f"Failed to retrieve releases from {releases_url}. Status code: {response.status_code}")

if __name__ == "__main__":
    update()
