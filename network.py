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

        if initial_values is not None: #if statement
            for key, value in initial_values.items(): #items can be iterated over the list of key values
                self.add_password(key, value) #for end-users to add passwords 

    def load_password_file(self, path): #this function loads the password file for the password dictionary to be the content of the file once it is decrypted   
        self.password_file = path  #add password to existing file
         
        try:
           with open(path, 'r') as f: #open the path in reading mode 
               for line in f:  #decrypt each line in the password file       
                   site, encrypted = line.split(":") #the colon separates each key value
                   fernet_obj = Fernet(self.key) 
                   decrypted = fernet_obj.decrypt(encrypted.encode()).decode() #decrypting passwords
                   self.password_dict[site] = decrypted #load the password to the respective site 
        except Exception as e: 
           print(f"Error loading password file: {e}") #error message when the programme cannot load the password file

    def add_password(self, site, password): #adding the password  
        self.password_dict[site] = password #adding password to the dictionary

        if self.password_file is not None: #password file has value which is input by the user
            with open(self.password_file, 'a+') as f: #helps the end-user write their passwords with the passwords being overwritten  
                encrypted = Fernet(self.key).encrypt(password.encode()) #makes sure that Fernet is used for encrypting and decrypting passwords
                f.write(site + ":" + encrypted.decode() + "\n") #allows the passwords to the written and encrypt the passwords and the line break indicates that there is a password for each line

    def get_password(self, site): #password for the site or identifier
        return self.password_dict[site] #the password returns to the dictionary

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

    while not done: #while the user is still within the programme these are the options proivded and the outcome that is expected to be produced

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
            if not os.path.isfile() : 
                print(f"The file '{path}' does not exist.")
            else:
                pm.load_password_file()
        elif choice == "5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("What site do you want: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Bye")
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()