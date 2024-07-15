import curses
import threading
import socket

def main(stdscr):
    try:
        curses.echo(True)  # Disable automatic echoing of keys to the screen
        stdscr.nodelay(False)  # Set the window to wait for user input

        input_win_height = 1
        input_win = curses.newwin(input_win_height, curses.COLS, curses.LINES - input_win_height, 0)
        input_win.keypad(True)
        
        output_win = curses.newwin(curses.LINES - input_win_height, curses.COLS, 0, 0)
        output_win.scrollok(True)  # Enable scrolling for output window
        output_win.idlok(True)  # Enable hardware line deletion/insertion if available
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind(("localhost", 65430))
        socket_server.listen(10)
        client_sock, client_addr = socket_server.accept()
        print(f"Connected to {client_addr}")
        def reader_thread():
            while True:
                # Your code to receive messages here, for example:
                # message = receive_message()
                message = client_sock.recv(1024).decode()
                output_win.addstr(message)
                output_win.refresh()

        # Start the reader thread
        t = threading.Thread(target=reader_thread, daemon=True)
        t.start()

        while True:
            input_win.clear()  # Clear the input window before displaying the prompt
            input_win.addstr("Enter message: ")
            input_win.refresh()  # Refresh after clearing and adding text
            input_str = input_win.getstr().decode()  # Get the user input
            input_win.clear()  # Clear after sending
            input_win.refresh()  # Refresh to show the cleared line
            with open("test.txt", "ab") as f:
                f.write(b"{input_str}")
    except KeyboardInterrupt:
        socket_server.close()
        exit()
if __name__ == '__main__':
    curses.wrapper(main)
