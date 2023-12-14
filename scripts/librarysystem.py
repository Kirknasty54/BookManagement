import sqlite3
import hashlib
import book as book
import user as user
import os
import customtkinter as ctk
import tkinter as tk
from user import User
conn = sqlite3.connect('user_accounts.db')
cursor = conn.cursor()
canlogin = False
# set our colors/modes, title of the application and default size on launch
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title('The Library of Kirkandria')
app.geometry("500x350")

class LibrarySystem:

    def __init__(self, users, books, current_user):
        self.__users = users
        self.__books = books
        self.__current_user = current_user

    @staticmethod
    def login_check(username, password):
        if username != '' and password != '':
            cursor.execute('select password from user_table where username=?', [username])
            result = cursor.fetchone()
            if result:
                if User.check_password(result[0], password):
                    canlogin=True
                    print('logged in successfully ')
                else:
                    print('incorrect password')
            else:
                print('This username doesn\'t exist, please register')


    def logout(self):
        pass

    def search_books(self, title, author):
        pass

    def remove_book(self, book_id):
        pass

    @staticmethod
    def register_user(username, password):
        cursor.execute("insert into user_table(username, password, role, books_borrowed) VALUES(?, ?, 'Member', 'None')", (username, User.hash_password(password)))
        conn.commit()
        print('register success')

    def borrow_book(self, username, book_id):
        pass

    def return_book(self, username, book_id):
        pass

    @staticmethod
    def loginScreen():
        # create a loginFrame that we will insert our prompts for username and password, and buttons for either logging in or registering
        loginFrame = ctk.CTkFrame(master=app)
        # loginImg = ctk.CTkImage(image=os.path.join('../scripts', 'loginimg.jpg')).pack(side='left')

        loginFrame.pack(pady=20, padx=60, fill='both', expand=True)

        label = ctk.CTkLabel(master=loginFrame, text='Login System')
        label.pack(pady=12, padx=10)

        usernameEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Username')
        passwordEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Password')
        usernameEntry.pack(pady=12, padx=10)
        passwordEntry.pack(pady=12, padx=10)

        loginButton = ctk.CTkButton(master=loginFrame, text='Login',command=lambda: LibrarySystem.login_check(usernameEntry.get(), passwordEntry.get()))
        if(canlogin):
            LibrarySystem.mainmenuScreen()
        registerButton = ctk.CTkButton(master=loginFrame, text='Register',command=lambda: LibrarySystem.register_user(usernameEntry.get(), passwordEntry.get()))

        loginButton.pack(pady=12, padx=10)
        registerButton.pack(pady=12, padx=10)
        app.mainloop()

    def mainmenuScreen(self):
        pass

    def addBookScreen(self):
        pass

    def removeBookScreen(self):
        pass

    def borrowBookScreen(self):
        pass

    def registerScreen(self):
        pass

    def searchScreen(self):
        pass