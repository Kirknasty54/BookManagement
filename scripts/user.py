from hashlib import sha256

class User:
    def __init__(self, username, password, role, borrowed_books):
        self.__username = username
        self.__password = self.hash_password(password)  # Hash the password during initialization
        self.__role = role
        self.__borrowed_books = borrowed_books

    #hashes the password using sha256 making it more secure
    @staticmethod
    def hash_password(password):
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password

    #checks the password entered in through the parameters to see if it returns the same hashed value as the user's password
    @staticmethod
    def check_password(hashed_password, password): return hashed_password == User.hash_password(password)

    #simply returns the role of the user to know if we should create the member main screen or the librianian main screen
    def get_role(self): return self.__role

    #this is a member only screen/function
    def borrow_book(self):
        pass