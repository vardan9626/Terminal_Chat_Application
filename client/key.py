from fernet import Fernet
import argparse

class key():
    def __init__(self, create_key=False) -> None:
        if create_key == True: 
            self.key = Fernet.generate_key()
            self.save_key(self.key)
            
        else:
            self.key = self.load_key()
        
    def load_key(self):
        with open("key.key", "rb") as f:
            return f.read()
        
    def save_key(self, key):
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    
    def encrypt_message(self, message):
        f = Fernet(self.key)
        return f.encrypt(message.encode())


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate or load a key")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a new key")
    args = parser.parse_args()
    if(args.generate):
        key(create_key=True)
    
    password = input("Enter a password: ")
    print(key().encrypt_message(password))