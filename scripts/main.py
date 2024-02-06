import json
import pandas as pd
import urllib.request
import textwrap
import csv
import sqlite3
import requests
from librarysystem import LibrarySystem

def main():


    with sqlite3.connect('user_accounts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user_table(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'username TEXT NOT NULL UNIQUE, '
                       'password TEXT NOT NULL,'
                       'role TEXT NOT NULL)')
        conn.commit()
        cursor.execute('CREATE TABLE IF NOT EXISTS book_transaction(user_id INTEGER NOT NULL,'
                       'book TEXT NOT NULL,'
                       'state TEXT NOT NULL,'
                       'FOREIGN KEY (user_id) REFERENCES user_table (id))')
    with sqlite3.connect('book_list.db') as conn:
        cursor = conn.cursor()
        sql_query = 'UPDATE book_registery SET quantity = 100'
        cursor.execute(sql_query)

    #this kickstarts the whole program
    LibrarySystem.loginScreen()

    #"UPDATE user_table SET books_borrowed = ? WHERE id = ?"
    #conn2 = sqlite3.connect('book_list.db')
    #cursor = conn2.cursor()

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
                   'quantity integer default 100)')'''

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

    #cursor.execute('selectisbn13 from book_registery')
    #cursor.execute('select isbn13 from book_registery limit -1 offset 9727')
    #isbn13s = [row[0] for row in cursor.fetchall()]

    #go through all the isbn13s and update the desc of the book in the database to the desc retrived by the google api
    #for isbn13 in isbn13s:
    #    desc = getBookDesc(isbn13)
    #    cursor.execute('update book_registery set desc = ? where isbn13 = ?', (desc, isbn13))
    #    conn2.commit()
    #conn2.commit()
    #cursor.execute("DELETE from book_registery where desc is NULL or trim(desc)=''")
    #conn2.commit()
main()