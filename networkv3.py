from cryptography.fernet import Fernet 
import os
#'Fernet' class is imported from the 'cryptography.fernet' module.
#The program imports the os module from the Raspberry Pi OS functionality.
class PasswordManager:
   
    def __init__(self): 
        self.key = None 
        self.password_file = None 
        self.password_dict = {} 
        #This function enables the password manager to create an empty password dictionary and an encryption key by default.
    
    def create_key(self, path): 
        self.key = Fernet.generate_key() 
        with open(path, 'wb') as f: 
            f.write(self.key)
        #This function uses Fernet to generate an encryption key for each specified file.  
    def load_key(self, path): 
        with open(path, 'rb') as f:  
            self.key = f.read() 
        #This function loads and decrypts the encyrption key of the specified file.
    def create_password_file(self, path, initial_values=None): 
        self.password_file = path 
       #This password file path enables password-related functions.
        if initial_values is not None: 
            for key, value in initial_values.items(): 
                self.add_password(key, value)  
        #If the end-user has created a password, the list of passwords and its accounts must be iterated and the end-user must be allowed to add passwords.
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
   
def main(): #This is the function that will accept the input of the end-user and produce an output.  The options listed in print("""""") will be shown on the command terminal of visual studio code.
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
    """) #These are the list of options provided by the program.
    done = False

    while not done: 
    #While this function is within the loop.  The code provides the list of options below.   
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        #When the end-user selects option 1, the password manager will create an encryption key.
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        #When the end-user selects option 2, the password manager will load the encryption key. 
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        #When the end-user selects option 3, the password manager will create a password file. 
        elif choice == "4":
            path = input("Enter path: ")       
            # Check if the file exists
            if not os.path.isfile(path) : 
                print(f"The file '{path}' does not exist.")
            else:
                pm.load_password_file(path)
        #When the end-user selects option 4, the password manager will load a password file, but an error message will be produced if
        #the password file does not exist.
        elif choice == "5":
            site = input("Enter the site: ")
            if not site.isalnum():
                print(f"Alphanumeric characters are required for the site name")
                #An error message will be produced when the end-user types non-alphanumeric characters.
            else:        
                password = input("Enter the password: ")            
                if len(password) < 12:
                    print("weak password length")
                else: 
                    print("suitable password length")
                    pm.add_password(site, password) #This if/else statement informs the end-user whether their password is suitable depending 
                    #on its length.
        #When the end-user selects option 5, they will be asked to enter a site before entering a password.
        elif choice == "6":
            site = input("What site do you want: ")
            if site.isalnum():
                  password = pm.get_password(site) #The password manager will retrieve a password from a site typed by the end-user.
            else:
                print("Error: Alphanumeric characters are required for the site name.")#An error message will be produced when non-alphanumeric characters are typed.
              
        #When the end-user selects option 6, they will receive the password they wanted after typing a site on the input field.
        elif choice.lower() == "q":
              done = True
              print("Bye")
        #The end-user types "q" or "Q" to quit the program and the program will say "Bye"
        else:
            print("Invalid choice!")
        #If the end-user types anything other than the number 1-6 or "q/Q", an error message, "Invalid Choice" will be produced.

if __name__ == "__main__":
    main()
#This enables the program to run