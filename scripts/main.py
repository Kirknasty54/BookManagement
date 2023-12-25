import os
import re
import json
import pandas as pd
import urllib.request
import textwrap
import csv
import sqlite3

import requests

from librarysystem import LibrarySystem

def main():
    LibrarySystem.loginScreen()
    '''conn = sqlite3.connect('user_accounts.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user_table(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'username TEXT NOT NULL UNIQUE, '
                   'password TEXT NOT NULL,'
                   'role TEXT NOT NULL,'
                   'books_borrowed TEXT,'
                   'prev_borrowed TEXT)')
    conn.commit()'''

    conn2 = sqlite3.connect('book_list.db')
    cursor = conn2.cursor()

    #this table is created to store our book information, to fill this database i used a csv from kaggle that had around 110000 books
    #could have done a even larger data set but this works for now
    '''cursor.execute('create table if not exists book_registery('
                   'id integer primary key autoincrement,'
                   'title text not null,'
                   'authors text not null,'
                   'publisher text not null,'
                   'publication_date text not null,'
                   'desc text,'
                   'isbn13 text,'
                   'quantity integer default 10)')'''
    #i extracted the titles, publisher, publication date, isbn-13, and authors from the csv file, by transferring only the desired columns to a pandas dataset
    #using the extracted isbn 13, i use it to search via the googlebooks api to add a desc to my database for every book
    #data = pd.read_csv('books - books.csv')
    #data = data[['title', 'authors', 'isbn13', 'publication_date', 'publisher']]
    #data.to_sql('book_registery', conn2, if_exists='append', index=False)

    #use the google api to retrieve the summary of the book based on the isbn13 number
    '''def getBookDesc(isbn13):
        url =  f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn13}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['volumeInfo'].get('description', '')'''
    #simply just 'download' the cover image to the images folder, so we can use it in the application
    '''def download_image(url, folder_path, filename):
        response = requests.get(url)
        with open(os.path.join(folder_path, filename), 'wb') as file:
            file.write(response.content)'''

    #use the google api to get the covers of the books
    '''def get_cover_url_by_isbn(isbn):
        base_url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': f'isbn:{isbn}'}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                volume_info = data['items'][0]['volumeInfo']
                cover_url = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else None
                return cover_url
        else:
            print(f"Error: {response.status_code}")
        return None'''

    #get the isbns from our data table so we can download the apprioaite isbn, probably should have implemented a imgurl column to see easier which books have covers and which dont
    #something for later maybe
    '''cursor.execute('SELECT isbn13 FROM book_registery limit -1 offset 6367')
    isbn_list = [row[0] for row in cursor.fetchall()]

    for isbn in isbn_list:
        cover_url = get_cover_url_by_isbn(isbn)
        if cover_url:
            print(f"Cover URL for ISBN {isbn}: {cover_url}")
            download_image(cover_url, os.path.join('..', 'images'), f"{isbn}.jpg")'''
    #cursor.execute('selectisbn13 from book_registery')
    #cursor.execute('select isbn13 from book_registery limit -1 offset 9727')
    #isbn13s = [row[0] for row in cursor.fetchall()]

    #go through all the isbn13s and update the desc of the book in the database to the desc retrived by the google api
    #for isbn13 in isbn13s:
    #    desc = getBookDesc(isbn13)
    #    cursor.execute('update book_registery set desc = ? where isbn13 = ?', (desc, isbn13))
    #    conn2.commit()
    #conn2.commit()

main()