import socket
import threading


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    recieved_data = ""
    try:
        while True:
            data = conn.recv(1024)
            # if not data:
            #     break
            # print(f"\nReceived from {addr}: {data.decode()}")
            recieved_data += data.decode()
            if '[[END]]' in data.decode():
                received_data = recieved_data.strip('[[END]]')
                with open("received_file", "wb") as f:
                    f.write(received_data.encode())
    except KeyboardInterrupt:
        print("Server shutting down.")
        conn.close()
    finally:
        conn.close()


def send(sock, addr):
    while True:
        message = input("Enter message: ")
        try:
            sock.sendall(message.encode())
        except KeyboardInterrupt:
            print("Error sending message.")
            sock.close()
            break


def server():
    host = '127.0.0.1'
    port = 10001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # create the socket
        s.bind((host, port))  # bind the socket
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread_read = threading.Thread(target=handle_client, args=(conn, addr))
            thread_write = threading.Thread(target=send, args=(conn, addr))
            thread_read.start()
            thread_write.start()


if __name__ == '__main__':
    server()
