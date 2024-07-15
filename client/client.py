import socket
import getpass
from key import key
from custom_print import print_col
import sys
import threading
import curses
import os


def get_x(stdscr, y):
    max_x = stdscr.getmaxyx()[1] - 1
    x = max_x
    while x > 0:
        char = stdscr.inch(y, x) & 0xFF
        if char not in (ord(' '), 0):
            break
        x -= 1
    return x + 1 if x > 0 else max_x + 1


class Connection:

    def __init__(self, client_socket, host, port) -> None:
        self.host = host
        self.port = port
        self.client_socket = client_socket
        self.columns = os.get_terminal_size().columns
        self.lock = threading.Lock()
        self.username_other_person = None

    def connect(self):
        '''
        This function is used to connect to the server and authenticate the user
        '''
        self.client_socket.connect((self.host, self.port))
        self.login()

    def send(self, message):
        self.client_socket.sendall(message.encode("utf-8"))

    def recieve(self):
        message = self.client_socket.recv(1024)  # Receive up to 1024 bytes
        if not message:
            return ""  # If no data is received, return an empty string
        return message.decode('utf-8')  # Decode the bytes to a string

    def login(self):
        """
        This function is used to authenticate the user with the server
        """
        try:
            print_col("Enter your username: ", color="yellow", end="")
            username = input()
            username = f"[[UNAME]]{username}[[UNAME]]"
            self.send(username)
            response = self.recieve()
            password = ""

            if "[[EXIST]]" in response:
                print_col("User already exists", color="green", bold=True)
                print("\033[33m", end="")
                sys.stdout.write("Enter ")
                sys.stdout.flush()
                password = getpass.getpass()
                print("\033[0m", end="")
            elif "[[NEW]]" in response:
                print_col("New User", color="green", bold=True)

                while True:
                    print("\033[33m", end="")
                    sys.stdout.write("Set ")
                    sys.stdout.flush()
                    password = getpass.getpass()
                    sys.stdout.write("Re-enter ")
                    sys.stdout.flush()
                    retyped_password = getpass.getpass()
                    print("\033[0m", end="")
                    if password != retyped_password:
                        print_col("\nPasswords do not match\n", "red", underline=True, italic=True)
                    else:
                        break
            elif "[[LOGGED_IN]]" in response:
                print_col("User already logged in", color="red", underline=True, italic=True)
                exit(1)
            else:
                print_col("You are not a valid user", color="red", underline=True, italic=True)
                exit(1)
            password = key().encrypt_message(password)
            password = f"[[PASS]]{password}[[PASS]]"
            self.send(password)

            response = self.recieve()
            if "[[AUTH]]" in response:
                print_col("Authenticated\n", color="green", bold=True)
                self.send("[[AUTHENTICATED]]")
                self.home()
            else:
                print_col("Authentication failed", color="red", underline=True, italic=True)
                exit(1)
        except KeyboardInterrupt:
            print_col("\nConnection closed", color="yellow", bold=True)
            self.send("[[LOGIN_FAILED]]")
            self.send("[[CONNECTION_CLOSED]]")
            exit()

    def home(self):
        """
        This function is used to provide the user with the base options
        """
        try:
            while True:
                print_col("This is the home screen of the chat application.\nYou can do the following operations "
                          "here:\n1. Chat with someone-C\n2. List of Online People-O\n3. All Users-A\n4. New files or "
                          "chats\n5. Logout-L\n6. Exit-E", color="cyan")
                print_col("\neg: To chat with someone, type C and press enter\n", color="cyan")
                print_col("Enter the option you want to choose: ", color="yellow", end="")
                option = input().upper()
                if option == "C":
                    print_col("\nPress Ctrl+C to go see other options\n", color="blue", bold=True)
                    self.chat()
                elif option == "O":
                    self.online_ppl()
                elif option == "A":
                    self.all_users()
                elif option == "N":
                    self.new_file_or_chat()
                elif option == "L":
                    self.logout()
                    break
                elif option == "E":
                    self.exit()
                else:
                    print_col("\nInvalid option\n", color="red", underline=True, italic=True)
        except KeyboardInterrupt:
            print_col("\nConnection closed", color="yellow", bold=True)
            self.send("[[CONNECTION_CLOSED]]")
            exit(1)

    def logout(self):
        """
        This function is used to logout the user
        """
        self.send("[[CONNECTION_CLOSED]]")
        print_col("Logged out", color="yellow", bold=True)

    def exit(self):
        """
        This function is used to exit the application
        """
        self.send("[[CONNECTION_CLOSED]]")
        print_col("Exiting", color="yellow", bold=True)
        exit(1)

    def chat(self):
        """
        This function is used to chat with the clients
        """
        try:
            while True:
                print_col("Enter the username of the person you want to chat with: ", color="yellow", end="")
                self.username_other_person = input()
                username = f"[[CHAT]]{self.username_other_person}[[CHAT]]"
                self.send(username)
                response = self.recieve()
                if "[[USER_NOT_FOUND]]" in response:
                    print_col("User not found", color="red", underline=True, italic=True)
                else:
                    break
            curses.wrapper(self.terminal_in_out)
        except KeyboardInterrupt:
            print_col("\nChoose one of the options:\n1) Transfer File to same person-T\n2) Go to Home-H",
                      color="yellow")
            option = input()
            if option == "T":
                print_col("Enter the path of your file: ", color="yellow", end="")
                path = input()
                self.transfer(path)
                print_col("Going back to home\n", color="cyan")

            elif option == "H":
                print_col("Going back to home\n", color="cyan")
            else:
                print_col("Invalid Option\n", color="red", underline=True, italic=True)
                print_col("Going back to home\n", color="cyan")

    def terminal_in_out(self, stdscr):
        t = None
        try:
            stdscr.idcok(True)
            stdscr.clear()
            stdscr.scrollok(True)
            stdscr.idlok(True)
            curses.curs_set(0)
            curses.cbreak()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Black text on white background
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White text on black background

            def reader_thread():
                while True:
                    try:
                        response = self.recieve()
                        if "[[CHAT_U]]" in response:  # my message
                            response = f"You:{response.split('[[CHAT_U]]')[1]}"
                        elif "[[CHAT_O]]" in response:  # other persons message
                            response = f"{self.username_other_person}:{response.split('[[CHAT_O]]')[1]}"
                        elif "[[FILE]]" in response:  # file transfer
                            # File Input begins
                            file_path = response.split('[[FILE]]')[1]
                            file_name = file_path.split('/')[-1]
                            if not os.path.exists(f"./files/{self.username_other_person}"):
                                os.mkdir(f"./files/{self.username_other_person}",0o777)
                            with open(f"./files/{self.username_other_person}/{file_name}", "wb") as f:
                                while True:
                                    file = self.client_socket.recv(1024)
                                    if not file:
                                        break
                                    f.write(file)
                            # File input ends
                            response = f"{self.username_other_person} is sending you a file named {file_name}"
                        elif "[[CLOSE_CHAT]]" in response:
                            return

                        # Critical section
                        curr_row, curr_col = stdscr.getyx()
                        stdscr.addstr(curr_row, 0, f"{response}\n")
                        # Critical section ends
                    except KeyboardInterrupt:
                        return

            t = threading.Thread(target=reader_thread, daemon=True)
            t.start()

            while True:
                row, col = stdscr.getmaxyx()
                key = stdscr.getch()
                if key == ord('i'):  # Insert mode
                    curr_row, curr_col = stdscr.getyx()
                    input_window = curses.newwin(1, col, row - 1, 0)
                    input_window.bkgd(' ', curses.color_pair(1))
                    input_window.scrollok(True)
                    input_window.idlok(True)
                    input_window.keypad(True)
                    curses.cbreak()
                    curses.curs_set(1)
                    s = ""
                    while True:
                        stdscr.refresh()
                        input_window.refresh()
                        key = input_window.getch()
                        if key == 27:  # Escape key
                            input_window.clear()
                            input_window.refresh()
                            input_window.bkgd(' ', curses.color_pair(2))
                            input_window.refresh()
                            curses.curs_set(0)
                            del input_window
                            break
                        elif key == curses.KEY_BACKSPACE or key == 127:
                            y, x = input_window.getyx()
                            if x == 0:
                                if y == 0:
                                    continue
                                input_window.move(y - 1, get_x(input_window, y - 1) - 1)
                                y, x = input_window.getyx()
                                x += 1
                            input_window.delch(y, x - 1)
                            if len(s):
                                s = s[:-1] if s[-1] != "\n" else s[:-2]
                        elif key == curses.KEY_ENTER or key == 10:
                            input_window.clear()
                            input_window.refresh()
                            input_window.refresh()

                            # Critical section starts
                            if len(s):
                                stdscr.addstr(curr_row, 0, f"{s}\n")
                            #     for server side send this to server with some tags around it
                                self.send(f"[[MSG]]{s}[[MSG]]")

                            curr_row, _ = stdscr.getyx()
                            s = ""
                            # Critical section ends

                            stdscr.refresh()
                        else:
                            input_window.addch(key)
                            s += chr(key)
        except KeyboardInterrupt:
            self.send("[[CLOSE_CHAT]]")
            if t and t.is_alive():
                t.join()
            # Properly restore the terminal settings and close curses windows
            raise

    def transfer(self, path):
        """
        This function is used to transfer files between the clients
        """
        if not os.path.exists(path):
            print_col("Path doesn't exist\n", color="red", underline=True, italic=True)
            return
        self.send("[[BEGIN_TRANSFER]]")
        with open(path, "rb") as f:
            while True:
                line = f.read(1024)
                if not line:
                    break
                self.client_socket.sendall(line)
        self.send("[[END_TRANSFER]]")


class client():

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        while True:
            server = Connection(self.client_socket, self.host, self.port)
            server.connect()


if __name__ == "__main__":
    host = "localhost"
    port = 65432
    client(host, port).connect()
