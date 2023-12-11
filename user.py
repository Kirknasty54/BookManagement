class User:
    def __init__(self, username, password, role, borrowed_books):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__borrowed_books = borrowed_books

    def hash_password(self, password):
        pass

    def check_password(self):
        pass

    def borrow_book(self):
        pass

