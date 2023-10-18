from cryptography.fernet import Fernet 
import os
#Importing crythography to encrypt and decrypt the password file and a os module from Raspberry Pi.
 #The code below runs the comments of the password manager
class PasswordManager:
   
    def __init__(self): 
        self.key = None 
        self.password_file = None 
        self.password_dict = {} 
#This function is an empty dictionary that does not specify a password file and generates an encryption key by default.
    
    def create_key(self, path): 
        self.key = Fernet.generate_key() 
        with open(path, 'wb') as f: 
            f.write(self.key)
#This function generates and encryption key that can be reused using the key method of Fernet.  
    def load_key(self, path): 
        with open(path, 'rb') as f:  
            self.key = f.read() 
#This function loads and decrypts the key generated
    def create_password_file(self, path, initial_values=None): 
        self.password_file = path 
    #This function enables any function in this programme that has a generated encryption key to run.
        if initial_values is not None: 
            for key, value in initial_values.items(): 
                self.add_password(key, value)  
        #If the end-user has created a password, the list of passwords and its accounts must be iterated and the end-user must be allowed to add paswwords.
    def load_password_file(self, path): 
        self.password_file = path  
    #After the passwords are decrypted, the system loads the password file to the password dictionary.     
        try:
           with open(path, 'r') as f:  
               for line in f:         
                   site, encrypted = line.split(":") 
                   fernet_obj = Fernet(self.key) 
                   decrypted = fernet_obj.decrypt(encrypted.encode()).decode() 
                   self.password_dict[site] = decrypted  
        except Exception as e: 
           print(f"Error loading password file: {e}") 
        #The function decrypts and loads passwords for the end-user on the respective site but an error will appear when the password cannot be loaded.  
    def add_password(self, site, password):   
        self.password_dict[site] = password 
   
        if self.password_file is not None: 
            with open(self.password_file, 'a+') as f: 
                encrypted = Fernet(self.key).encrypt(password.encode()) 
                f.write(site + ":" + encrypted.decode() + "\n") #allows the passwords to the written and encrypt the passwords and the line break indicates that there is a password for each line
        #This function allows the end-user to add passwords to their password dictionary.  Their passwords will be encrypted and decrypted by Fernet.
    def get_password(self, site): 
        return self.password_dict[site] 
    #The password of the site will be returned to the password dictionary.
def main(): #list of passwords stored for email, instagram, youtube, and something else
    password = {
        "email": "1234567",
        "instagram": "myigpassword",
        "youtube": "helloworld123",
        "something": "myfavoritepassword_123"
    }
    pm = PasswordManager()
    print("""What do you want to do? 
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit                         
    """) #a question with a list of choices provided by the programme
    done = False

    while not done: 
       
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")       
            # Check if the file exists
            if not os.path.isfile(path) : 
                print(f"The file '{path}' does not exist.")
            else:
                pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")            
            if len(password) < 12:
                print("weak password length")
            else: 
                print("suitable password length")
                pm.add_password(site, password)
        elif choice == "6":
            site = input("What site do you want: ")
        elif choice.lower() == "q":
              done = True
              print("Bye")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
#This enables the programme to run