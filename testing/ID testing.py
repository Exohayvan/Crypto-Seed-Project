import hashlib
import base64

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

btw_address = "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"
user_id = generate_id(btw_address)
print(f"Shortened User ID for BTW address '{btw_address}': {user_id}")
