import socket
import threading


def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    try:
        
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            try:
                print(f"Received from {client_address}: {message.decode()}")
            except UnicodeDecodeError:
                print(f"Received from {client_address}: {message}")
            if("[[UNAME]]" in message.decode('utf-8')):
                client_socket.sendall("[[NEW]]".encode("utf-8"))
            elif "[[PASS]]" in message.decode('utf-8'):
                client_socket.sendall("[[AUTH]]".encode("utf-8"))
            # client_socket.sendall(message)
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")

def server():
    host = '127.0.0.1'  # Server's IP address
    port = 65432        # Port to listen on (non-privileged ports are > 1023)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server is listening on", host, port)
        
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")

if __name__ == '__main__':
    server()
