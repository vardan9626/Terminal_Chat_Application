import socket

def receive_file(filename, host='0.0.0.0', port=12345):
    # Create a socket object
    s = socket.socket()
    # Bind to the host and port
    s.bind((host, port))
    # Listen for incoming connections
    s.listen(5)
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    # Open a file to write in binary mode
    with open(filename, 'wb') as file:
        # Receive data and write to the file
        while True:
            data = conn.recv(1024)  
            if not data:
                break
            file.write(data)

    # Close connection
    conn.close()
    print("File received successfully.")

# Run the server function
receive_file('resume')
