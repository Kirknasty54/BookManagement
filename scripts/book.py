import json
from urllib.request import urlopen

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__quantity = quantity

    @staticmethod
    def getImgUrl(isbn):
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        response = urlopen(api+isbn)
        book_info = json.load(response)
        if 'items' in book_info:
            vol_info = book_info['items'][0]['volumeInfo']
            if 'imageLinks' in vol_info:
                if 'thumbnail' in vol_info['imageLinks']:
                    url = vol_info['imageLinks']['thumbnail']
                    return url
                else:
                    return vol_info['imageLinks']['smallThumbnail']
        else:
            url = 'https://t3.ftcdn.net/jpg/02/16/67/50/360_F_216675048_39petQYPtJ9cv5ycUg1LOmCtcNCoqtdk.jpg'
            return url