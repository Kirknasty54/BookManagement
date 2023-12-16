import sqlite3
from librarysystem import LibrarySystem
def main():
    LibrarySystem.loginScreen()
    conn = sqlite3.connect('user_accounts.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user_table(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'username TEXT NOT NULL UNIQUE, '
                   'password TEXT NOT NULL,'
                   'role TEXT NOT NULL,'
                   'books_borrowed TEXT,'
                   'prev_borrowed TEXT)')
    conn.commit()
    #cursor.execute("insert into user_table(username, password, role, books_borrowed) VALUES('u1', 'p1', 'Member', 'None')")
    '''conn2 = sqlite3.connect('book_list.db')
    cursor = conn2.cursor()
    cursor.execute('create table if not exists book_registery('
                   'book_id integer not null unique,'
                   'title text not null,'
                   'author text not null,'
                   'quantity integer not null)')
    conn2.commit()'''
main()