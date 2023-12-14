class Book:
    def __init__(self, book_id, title, author, quantity):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__quantity = quantity

    def update_quantity(self, change):
        self.__quantity += change
