import json
import re
import hashlib
import base64

def is_valid_btc_address(btc):
    pattern = '^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$'
    return re.match(pattern, btc) is not None

def generate_id(btc, id_length=12):
    # Create SHA-512 hash object
    hasher = hashlib.sha512()

    # Update the hash object with the address bytes
    hasher.update(btc.encode('utf-8'))

    # Get the binary representation of the hash
    binary_hash = hasher.digest()

    # Encode the binary hash using base64
    base64_hash = base64.b64encode(binary_hash).decode('utf-8')

    # Remove any non-alphanumeric characters and truncate to the desired length
    alphanumeric_hash = ''.join(c for c in base64_hash if c.isalnum())
    short_id = alphanumeric_hash[:id_length]

    return short_id

def ask_run():
    choices = {
        "1": "Solo (Not Recommended)",
        "2": "Worker (Recommended)",
        "3": "Node (Experienced users only | Not Recommended)"
    }

    print("How would you like to run this program?")
    print("(If unsure choose 'Worker')")
    for key, value in choices.items():
        print(f"{key}) {value}")

    user_choice = input("Enter your choice (1, 2, or 3): ")

    while user_choice not in choices:
        print("Invalid choice. Please choose either 1, 2, or 3.")
        user_choice = input("Enter your choice (1, 2, or 3): ")

    return choices[user_choice]

def data_json():
    version = "1.0"  # Replace with your desired version

    try:
        with open('data.json', 'r') as file:
            json_data = json.load(file)
            jversion = json_data.get('version')
            btc = json_data.get('btc')
            is_node = json_data.get('is_node')
            run_mode = json_data.get('run_mode')
    except FileNotFoundError:
        jversion = version

        while True:
            btc = input('Please enter a BTC address: ')
            if is_valid_btc_address(btc):
                break
            else:
                print('Invalid BTC address. Please try again.')

        run_mode = ask_run()

        data = {
            "version": jversion,
            "btc": btc,
            "is_node": False,
            "run_mode": run_mode
        }

        with open('data.json', 'w') as file:
            json.dump(data, file)

    else:
        if jversion != version:
            json_data['version'] = version
            with open('data.json', 'w') as file:
                json.dump(json_data, file)

    userID = generate_id(btc)

    return jversion, btc, is_node, run_mode, userID
