from cryptography.fernet import Fernet
import os
import time
import platform
from datetime import datetime

"""
message = "are you a user?"


key = Fernet.generate_key()
fernet = Fernet(key)

encrypted_message = fernet.encrypt(message.encode())
decrypted_message = fernet.decrypt(encrypted_message).decode()

print(encrypted_message)
print(decrypted_message)
"""


class User:
    def __init__(self, username):
        self.username = username
        self.fernet = None
        self.folders = ["message", "cipher", "decipher"]

    def user_exists(self):
        if not os.path.exists(self.username):
            return False
        else:
            return True

    def generate_key(self):
        # Create the folder if it doesn't exist
        if not os.path.exists(self.username):
            os.makedirs(self.username)
            for folder in self.folders:
                os.makedirs(f"{self.username}/{folder}")
        else:
            return False

        # Create the file inside the folder
        file_path = os.path.join(self.username, "key.txt")

        key = Fernet.generate_key()
        with open(file_path, "wb") as key_file:
            key_file.write(key)
        self.fernet = Fernet(key)

        return True

    def load_key(self):
        key = None
        file_path = os.path.join(self.username, "key.txt")
        with open(file_path, "rb") as key_file:
            key = key_file.read()
        self.fernet = Fernet(key)
        return True


class Login(User):
    def __init__(self, username):
        super().__init__(username)  # Call the Parent's constructor

    def login(self):
        if not super().user_exists():
            return False
        return super().load_key()


class Register(User):
    def __init__(self, username):
        super().__init__(username)  # Call the Parent's constructor

    def register(self):
        if super().user_exists():
            return False
        return super().generate_key()


class Run:
    def __init__(self):
        self.user = None

    def startpi(self):
        # Display pi menu
        print("Menu:")
        print("1. login")
        print("2. register")
        print("3. quitpi")

    def login(self):
        username = input("Enter the username: ")
        self.user = Login(username)
        if self.user.login():
            print("Login Successful.")
            self.logan()
        else:
            print("No user found.")
            self.startpi()

    def register(self):
        username = input("Enter the username: ")
        self.user = Register(username)
        if self.user.register():
            print("Register Successful.")
            self.logan()
        else:
            print("User exists already.")
            self.startpi()

    def quitpi(self):
        print("Exiting pi...")

    def startlogan(self):
        # Display menu
        print("1. message")
        print("2. encrypt")
        print("3. decrypt")
        print("4. quit")

    def message(self):
        filename = input("Enter filename(default):")
        if filename == "":
            filename = "default"
        # Generate a filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(
            self.user.username, os.path.join("message", f"{filename}_{timestamp}.txt")
        )
        # Check if the file exists
        if not os.path.exists(file_path):
            # Create the file if it doesn't exist
            with open(file_path, "w") as openfile:
                openfile.write("")
            # Determine the operating system
            system_platform = platform.system()
            print(f"Opened file: {file_path}")

            if system_platform == "Windows":
                os.startfile(file_path)  # Windows-specific
            elif system_platform == "Darwin":  # macOS
                os.system(f"open {file_path}")
            else:  # Linux and others
                os.system(f"xdg-open {file_path}")
        else:
            print("file already exist")

    def encrypt(self):
        folder_path = os.path.join(self.user.username, "message")
        # Get all entries in the directory
        entries = os.listdir(folder_path)

        # Filter and list only files
        files = [
            file for file in entries if os.path.isfile(os.path.join(folder_path, file))
        ]
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        file = int(input("Select file to encrypt:"))
        file_path = os.path.join(self.user.username, "message", files[file - 1])

        # Read message from file
        with open(file_path, "r") as data:
            message = data.read()

        # Encrypt the message
        encrypted_message = self.user.fernet.encrypt(message.encode())

        encrypted_filename = f"{files[file-1]}_ciphertext.txt"
        encrypt_path = os.path.join(self.user.username, "cipher", encrypted_filename)
        print(encrypt_path)
        # Write encrypted message to a new file
        with open(encrypt_path, "wb") as encrypter:
            encrypter.write(encrypted_message)

    def decrypt(self):
        folder_path = os.path.join(self.user.username, "cipher")
        # Get all entries in the directory
        entries = os.listdir(folder_path)

        # Filter and list only files
        files = [
            file for file in entries if os.path.isfile(os.path.join(folder_path, file))
        ]
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        file = int(input("Select file to decrypt:"))
        file_path = os.path.join(self.user.username, "cipher", files[file - 1])

        # Read message from file
        with open(file_path, "r") as data:
            message = data.read()

        # Decrypt the message
        decrypted_message = self.user.fernet.decrypt(message).decode()

        decrypted_filename = f"{files[file-1]}_deciphertext.txt"
        decrypt_path = os.path.join(self.user.username, "decipher", decrypted_filename)

        # Write decrypted message to a new file
        with open(decrypt_path, "w") as decrypter:
            decrypter.write(decrypted_message)

    def quitlogan(self):
        print("Exiting logan...")
        # self.pi()

    def case_default(self):
        print("Invalid selection.")
        time.sleep(1)

    def pi(self):
        self.startpi()

        # Simulating a switch-case using a dictionary
        switchpi = {"1": self.login, "2": self.register, "3": self.quitpi}

        try:
            while True:
                # User input
                choice = input("Enter your choice (3. Close): ").strip()

                # Execute the corresponding function
                action = switchpi.get(choice, self.case_default)
                action()

                # Exit condition
                if choice == "3":
                    break
        except Exception as e:
            print(f"Error: {e}")

    def logan(self):
        self.startlogan()

        # Simulating a switch-case using a dictionary
        switchlogan = {
            "1": self.message,
            "2": self.encrypt,
            "3": self.decrypt,
            "4": self.quitlogan,
        }

        try:
            while True:
                # User input
                choice = input("Enter your choice (4. Close): ").strip()

                # Execute the corresponding function
                action = switchlogan.get(choice, self.case_default)
                action()

                # Exit condition
                if choice == "4":
                    break
        except Exception as e:
            print(f"Error: {e}")


# Main function to handle user options
def main():
    # files = ["message", "cipher", "decipher"]
    # for folder in files:
    #     os.makedirs(f"ls/{folder}")
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # file_path = os.path.join("self.user.username", os.path.join("message", f"_{timestamp}"))
    # print(timestamp)
    # print(file_path)
    # folder_path = os.getcwd()
    # # Get all entries in the directory
    # entries = os.listdir(folder_path)

    # # Filter and list only files
    # files = [
    #     file for file in entries if os.path.isfile(os.path.join(folder_path, file))
    # ]
    # print(files)
    # with open("encrypt_path", "w") as encrypter:
    #     encrypter.write("encrypted_message")
    window = Run()
    window.pi()


# Run the main function
if __name__ == "__main__":
    main()
