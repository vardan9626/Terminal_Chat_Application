import socket

def send_file(filename, host='localhost', port=12345):
    # Create a socket object
    s = socket.socket()
    # Connect to the server
    s.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Open the file to read in binary mode
    with open(filename, 'rb') as file:
        # Read and send the entire file
        while True:
            data = file.read(1024)
            if not data:
                break
            s.send(data)

    # Close the socket
    s.close()
    print("File sent successfully.")

# Run the client function with the path to the file you want to send
send_file('/home/vardan/Downloads/pdf_files/my_iitb_resume.pdf')
