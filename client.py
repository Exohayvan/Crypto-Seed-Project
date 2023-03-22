import socket
import select

MDNS_ADDR = '224.0.0.251'  # mDNS multicast address
MDNS_PORT = 5353
QUERY_NAME = '_my-service._tcp.local'

def discover_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind(('', MDNS_PORT))

        # Send mDNS query for the service name
        query = bytearray()
        query += b'\x00\x00'  # Transaction ID
        query += b'\x00\x00'  # Flags
        query += b'\x00\x01'  # Questions
        query += b'\x00\x00'  # Answer RRs
        query += b'\x00\x00'  # Authority RRs
        query += b'\x00\x00'  # Additional RRs
        for label in QUERY_NAME.split('.'):
            query += bytes([len(label)])
            query += label.encode('ascii')
        query += b'\x00'  # End of domain name
        query += b'\x00\x21'  # QTYPE: PTR
        query += b'\x00\x01'  # QCLASS: IN

        udp_socket.sendto(query, (MDNS_ADDR, MDNS_PORT))

        # Receive mDNS response and extract IP address
        while True:
            r, w, x = select.select([udp_socket], [], [], 1)
            if r:
                response, address = udp_socket.recvfrom(1024)
                if response[2] & 0x80:
                    continue  # Ignore non-response packets
                offset = response.find(b'\x00\x0c\x00\x01')  # Type: PTR, Class: IN
                if offset < 0:
                    continue  # Ignore packets without PTR record
                offset += 6  # Skip TTL
                length = response[offset]
                hostname = response[offset + 1:offset + 1 + length].decode('ascii')
                if hostname.endswith(QUERY_NAME):
                    offset = response.find(b'\x00\x01\x00\x01')  # Type: A, Class: IN
                    if offset < 0:
                        continue  # Ignore packets without A record
                    offset += 10  # Skip TTL and RDLENGTH
                    ip_address = socket.inet_ntoa