import socket
import threading
import os


class Connection:

    def __init__(self, client_socket, host, port) -> None:
        self.host = host
        self.port = port
        self.client_socket = client_socket

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        self.transfer()

    def send(self, message):
        self.client_socket.sendall(message.encode("utf-8"))

    def transfer(self):
        file_path = input("enter the path of the file you want to transfer")
        if not os.path.exists(file_path):
            print("Path does not exist")
            return
        with open(file_path, "rb") as fl:
            while True:
                data = fl.read(1024)
                if not data:
                    self.send("[[END]]")
                    break
                self.client_socket.sendall(data)


class Client:

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        print("Trying to connect")
        while True:
            server = Connection(self.client_socket, self.host, self.port)
            server.connect()


if __name__ == '__main__':
    tmp = Client("127.0.0.1", 10001)
    tmp.connect()

