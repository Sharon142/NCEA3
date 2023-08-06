from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self) -> None:
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self , path):  
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:

            f.write(self.key)