import socket
import time

def send_message(message,s):
    s.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 65430))
    tmp=0
    num_lines=0
    while True:
        tmp=num_lines
        with open("test.txt", "r") as f:
            line = f.readlines()
            for i in range(num_lines,len(line)):
                send_message(line[i],s)
                num_lines+=1
        time.sleep(0.1)
    s.close()