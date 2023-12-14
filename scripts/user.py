from hashlib import sha256

class User:
    def __init__(self, username, password, role, borrowed_books):
        self.__username = username
        self.__password = self.hash_password(password)  # Hash the password during initialization
        self.__role = role
        self.__borrowed_books = borrowed_books

    @staticmethod
    def hash_password(password):
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password

    @staticmethod
    def check_password(hashed_password, password):
        return hashed_password == User.hash_password(password)

    def borrow_book(self):
        pass