import libtorrent as lt
import time

# Create a session
ses = lt.session()

# Add a DHT router (a well-known node in the BitTorrent network)
ses.add_dht_router("router.bittorrent.com", 6881)
ses.add_dht_router("router.utorrent.com", 6881)

# Start the DHT
ses.start_dht()

# Use a unique info-hash for your application
info_hash = lt.sha1_hash(b"your_unique_application_identifier")

# Keep searching for peers with the same info-hash
while True:
    peers = ses.dht_get_peers(info_hash)
    for peer in peers:
        print(f"Discovered peer: {peer}")
    time.sleep(10)
