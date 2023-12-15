import sqlite3
from PIL import Image
import hashlib
import book as book
import user as user
import os
import customtkinter as ctk
from user import User
from CTkMessagebox import CTkMessagebox as ctkm

# set our colors/modes, title of the application and default size on launch
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title('The Library of Kirkandria')
app.geometry("500x350")

#this handles most of the logic of the overall app
class LibrarySystem:
    def __init__(self, users, books, current_user):
        self.__users = users
        self.__books = books
        self.__current_user = current_user

    #this is a login check, checks if the username and password have something entered in them, then we search the database for a matching record of username and matching password
    #if one is found, we return 0 so we can use this function for further logic
    #if a record is found with a matching username but mismatching password, then alert the user that it looks like the password was incorrect
    #if no record is found at all, then alert user that no username by that name exists and tell them to either correct it or register as a new user
    @staticmethod
    def login_check(username, password):
        if username != '' and password != '':
            result = ''
            with sqlite3.connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute('select password from user_table where username=?', [username])
                result = cursor.fetchone()
            if result:
                if User.check_password(result[0], password):
                    print('logged in successfully ')
                    #this will return if the user can sucessfully log in
                    return 0
                else:
                    ctkm(title='Incorrect Password', message='Looks like that password doesn\'t match try again', icon='warning', option_1='Close')
                    #this will return if the user entered in a correct username, but the password was found to be incorrect
                    return 1
            else:
                #this will return if the user enters a username that is not present in the user_accounts database
                ctkm(title='No user Exists', message='Looks like there is no username like that, you should register an account', icon='warning', option_1='Close')
                return -1

    #kicks the user out of their current frame and boots them back to the log in frame
    def logout(self):
        pass

    #a search feature of available books, generes, authors, etc, etc.
    def search_books(self, title, author):
        pass

    #this removes a book from the inventory, could be either from borrowing, or librianan removing book from inventory
    def remove_book(self, book_id):
         pass

    @staticmethod
    def register_user(username, password):
        user_exists = True
        with sqlite3.connect('user_accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM user_table WHERE username = ?", (username,))
            existing = cursor.fetchone()
            if not existing:
                ctkm(title='No user Exists', message='Looks like there is no username like that, you should register an account', icon='warning', option_1='Close')
                user_exists = False

        if user_exists:
            ctkm(title='Registration Error', message='A username by that name already exists, try fixing your password', icon='warning', option_1='Close')
        else:
            with sqlite3.connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute("insert into user_table(username, password, role, books_borrowed) VALUES(?, ?, 'Member', 'None')", (username, User.hash_password(password)))
                conn.commit()
            print('register success')

    def borrow_book(self, username, book_id):
        pass

    def return_book(self, username, book_id):
        pass

    @staticmethod
    def loginScreen():
        def on_login_clicked(username, password):
            canlogin = LibrarySystem.login_check(username, password)
            if canlogin == 0:
                loginFrame.destroy()
                currUser = LibrarySystem.get_curr_user(username, password)
                loggedUser = User(username=currUser['username'],
                                  password=currUser['password'],
                                  role=currUser['role'],
                                  borrowed_books=['books_borrowed'])
                if(loggedUser.get_role() == 'Member'):LibrarySystem.mainmenu_MemberScreen()

        def onRegisterClicked(username, password):
            pass

        #create a loginFrame that we will insert our prompts for username and password, and buttons for either logging in or registering
        loginFrame = ctk.CTkFrame(master=app)
        loginFrame.pack(pady=20, padx=60, fill='both', expand=True)

        img_path = os.path.abspath(os.path.join('..', 'images', 'logingimage.jpg'))

        #check if the image file exists
        if os.path.exists(img_path):
            #load the image using CTkImage
            imgframe = ctk.CTkFrame(master=app)
            imgframe.pack(side= 'left')
            img = ctk.CTkImage(dark_image=Image.open(img_path), size = (100, 100))

            #create a Label widget to display the image
            img_label = ctk.CTkLabel(master=imgframe, image=img, text='')
            img_label.pack(side='left')
        else:
            print(f"Image file not found: {img_path}")

        label = ctk.CTkLabel(master=loginFrame, text='Login System')
        label.pack(pady=12, padx=10)

        usernameEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Username')
        passwordEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Password')
        usernameEntry.pack(pady=12, padx=10)
        passwordEntry.pack(pady=12, padx=10)

        loginButton = ctk.CTkButton(master=loginFrame, text='Login',command=lambda: on_login_clicked(usernameEntry.get(), passwordEntry.get()))
        registerButton = ctk.CTkButton(master=loginFrame, text='Register',command=lambda: LibrarySystem.register_user(usernameEntry.get(), passwordEntry.get()))

        loginButton.pack(pady=12, padx=10)
        registerButton.pack(pady=12, padx=10)
        app.mainloop()

    @staticmethod
    def get_curr_user(username, password):
        with sqlite3.connect('user_accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_table WHERE username=? AND password=?', (username, User.hash_password(password)))
            result = cursor.fetchone()
            if result:
                user_info = {
                    'username': result[1],
                    'password': result[2],
                    'role': result[3],
                    'books_borrowed': result[4]
                }
                return user_info

    @staticmethod
    def mainmenu_MemberScreen():
        main_menu_frame = ctk.CTkFrame(master=app)
        main_menu_frame.pack(pady=20, padx=60, fill='both', expand=True)
        label=ctk.CTkLabel(master=main_menu_frame, text='Main Menu, Welcome Member')
        label.pack(pady=12, padx=10)

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