import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f'Server listening on {HOST}:{PORT}...')

    while True:
        client_socket, address = server_socket.accept()
        print(f'Connected by {address}')

        # Receive job from client
        job = client_socket.recv(1024)
        print(f'Received job: {job.decode()}')

        # Process job (e.g., run a script, execute a command)
        # ...

        # Send result to client
        result = b'Success'
        client_socket.sendall(result)
        client_socket.close()
