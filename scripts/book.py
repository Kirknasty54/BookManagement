import json
from io import BytesIO
from urllib.request import urlopen
import requests
from PIL import Image, ImageTk
from urlLabel import CTkUrlLabel

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__quantity = quantity

    def updateQuantity(self, change):
        self.__quantity += change

    @staticmethod
    def getImgUrl(frame, isbn):
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        #9780767910439
        response = urlopen(api+isbn)
        book_info = json.load(response)
        if 'items' in book_info:
            vol_info = book_info['items'][0]['volumeInfo']
            book_cover = CTkUrlLabel(master=frame, text='this is here')
            if 'imageLinks' in vol_info:
                book_cover.configure(url=vol_info['imageLinks']['thumbnail'])
                print(f"big pic: {vol_info['imageLinks']['thumbnail']}")
                return book_cover