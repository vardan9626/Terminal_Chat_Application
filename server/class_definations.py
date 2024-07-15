import socket
import threading

cnt = 0

class client_socket:
    def __init__(self, username, password):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = cnt+1
        cnt+=1
        self.username = username
        self.password = password
    
    def receive(self):
        while True:
            message = self.client_socket.recv(1024)
            if not message:
                break
            print(f"Received from {self.host}:{self.port}: {message.decode()}")
    
    def send(self, message):
        self.client_socket.sendall(message.encode())
    
    def close(self):
        self.client_socket.close()
        print(f"Connection closed with {self.host}:{self.port}")
