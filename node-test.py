import qBittorrent as lt
import time

# Function to read the key from the key.pem file
def read_key_from_file():
    with open('key.pem', 'r') as file:
        return file.read().strip()

# Create a session
ses = lt.session()

# Add a DHT router (a well-known node in the BitTorrent network)
ses.add_dht_router("router.bittorrent.com", 6881)
ses.add_dht_router("router.utorrent.com", 6881)

# Start the DHT
ses.start_dht()

# Read the key from the key.pem file
key = read_key_from_file()
info_hash = lt.sha1_hash(key.encode())

# Keep searching for peers with the same info-hash
while True:
    peers = ses.dht_get_peers(info_hash)
    for peer in peers:
        print(f"Discovered peer: {peer}")
    time.sleep(10)