import sqlite3
import tkinter
import webbrowser
from PIL import Image, ImageTk
import book as book
import user as user
from tkinter import PhotoImage
import os
import customtkinter as ctk
from user import User
from CTkMessagebox import CTkMessagebox as ctkm

# set our colors/modes, title of the application and default size on launch
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title('The Library of Kirkandria')
app.after(0, lambda : app.state('zoomed'))
icon = PhotoImage(file=os.path.join('..', 'images', 'icon.png'))
app.wm_iconbitmap()
app.iconphoto(False, icon)


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
        #checks if anything is actually in the username and password so we dont have unecessary checks for empty entry boxes
        #if user has entered in something, then we go through the possible outcomes
        #also we create a result variable that is initalized as empty, if a username is found with matching password, then allow the user to log in
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
                #if a username is found but incorrect password, alert user and have them try again
                else:
                    ctkm(title='Incorrect Password', message='Looks like that password doesn\'t match try again', icon='warning', option_1='Close')
                    #this will return if the user entered in a correct username, but the password was found to be incorrect
                    return 1
            #if no matching username is found at all, then this will execute alerting the user to register to account
            else:
                #this will return if the user enters a username that is not present in the user_accounts database
                ctkm(title='No user Exists', message='Looks like there is no username like that, you should register an account', icon='warning', option_1='Close')
                return -1

    #kicks the user out of their current frame and boots them back to the log in frame
    @staticmethod
    def logout(screen):
        screen.destroy()
        LibrarySystem.loginScreen()

    #a search feature of available books, generes, authors, etc, etc.
    def search_books(self, title, author):
        pass

    #this removes a book from the inventory, could be either from borrowing, or librianan removing book from inventory
    def remove_book(self, book_id):
         pass

    #registers the account based on the username and password entered
    @staticmethod
    def register_user(username, password):
        if username != '' and password != '':
            user_exists = True
            with sqlite3.connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM user_table WHERE username = ?", (username,))
                existing = cursor.fetchone()
                if not existing: user_exists = False

            if user_exists: ctkm(title='Registration Error', message='A username by that name already exists, try fixing your password', icon='warning', option_1='Close')
            else:
                with sqlite3.connect('user_accounts.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("insert into user_table(username, password, role, books_borrowed) VALUES(?, ?, 'Member', 'None')", (username, User.hash_password(password)))
                    conn.commit()
                ctkm(title='Registration Success', message='Account successfully registered', icon='check', option_1='Close')
        else: ctkm(title='No Entry Found', message='Please enter in a username and password to register an account', icon='warning', option_1='Close')

    def borrow_book(self, username, book_id):
        pass

    def return_book(self, username, book_id):
        pass

    #this is the first screen that appears upon startup and handles the log in logic
    #depending on the log in entered, the user will either go to the member main menu screen or the librianian main menu screen, both screens have some differing options and some of the same
    @staticmethod
    def loginScreen():
        def on_login_clicked(username, password):
            canlogin = LibrarySystem.login_check(username, password)
            if canlogin == 0:
                for child in list(app.children.values()):
                    child.destroy()
                currUser = LibrarySystem.get_curr_user(username, password)
                loggedUser = User(username=currUser['username'],
                                  password=currUser['password'],
                                  role=currUser['role'],
                                  borrowed_books=['books_borrowed'])
                if(loggedUser.get_role() == 'Member'):LibrarySystem.mainmenu_MemberScreen()

        img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('logingimage.jpg')), size=(400, 350))
        bg_label = ctk.CTkLabel(app, image=img, text='')
        bg_label.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(master=app, text='Login System')
        label.place(relx=0.5, rely=0.2, anchor='center')

        usernameEntry = ctk.CTkEntry(master=app, placeholder_text='Username')
        usernameEntry.place(relx=0.5, rely=0.3, anchor='center')
        passwordEntry = ctk.CTkEntry(master=app, show='*', placeholder_text='Password')
        passwordEntry.place(relx=0.5, rely=0.4, anchor='center')

        loginBtn = ctk.CTkButton(master=app, text='Login',command=lambda: on_login_clicked(usernameEntry.get(), passwordEntry.get()), corner_radius=32).place(relx=0.5, rely=0.5, anchor='center')
        registerBtn = ctk.CTkButton(master=app, text='Register',command=lambda: LibrarySystem.register_user(usernameEntry.get(), passwordEntry.get()), corner_radius=32).place(relx=0.5, rely=0.6, anchor='center')
        gitHubBtn = ctk.CTkButton(master=app, text='GitHub', command=lambda : webbrowser.open_new('https://github.com/Kirknasty54'), width=10, height=10).place(relx=0.0, rely=0.0)
        #websiteBtn = ctk.CTkButton(master=app, text='Website', command=lambda : webbrowser.open_new(''),width=10, height=10).place(relx=0.0, rely=0.1)

        def onResize(event):
            new_size = (app.winfo_width(), app.winfo_height())
            img.configure(size=new_size)

        app.bind('<Configure>', onResize)
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

    #this is the main menu screen for members only, gives them a variety of options like searching for books, borrowing books, returning books, and log out
    #might eventually add a recommendation system based on previously borrowed books
    @staticmethod
    def mainmenu_MemberScreen():
        main_menu_frame = ctk.CTkFrame(master=app)
        main_menu_frame.pack(pady=20, padx=60, fill='both', expand=True)
        label=ctk.CTkLabel(master=main_menu_frame, text='Main Menu\nWelcome Member')
        label.pack(pady=12, padx=10)
        search_bookBtn = ctk.CTkButton(master=main_menu_frame, text='Search for Books', command= lambda : onSearchClicked(), corner_radius=32).pack(pady=12, padx=10)
        return_book_Btn = ctk.CTkButton(main_menu_frame, text='Return Books', command= lambda : onReturnClicked(), corner_radius=32).pack(pady=12, padx=10)
        logout_Btn = ctk.CTkButton(main_menu_frame, text='Logout', command= lambda: LibrarySystem.logout(main_menu_frame), corner_radius=32).pack(pady=12, padx=10)

        def onSearchClicked():
            main_menu_frame.destroy()
            LibrarySystem.searchScreen()

        def onReturnClicked():
            main_menu_frame.destroy()
            LibrarySystem.returnBookScreen()

    #this will be a librianian only method/screen
    @staticmethod
    def addBookScreen():
        pass

    # this will be a librarian only method/screen
    @staticmethod
    def removeBookScreen():
        pass

    @staticmethod
    def returnBookScreen():
        pass

    #this will allow users to search the through the database of available books
    #have a progress bar to represent search progress
    #search screen will have a search bar to search by author, title, or isbn
    @staticmethod
    def searchScreen():

        search_screen_frame = ctk.CTkFrame(master=app, width=app._current_width/2, height=app._current_height/2).pack(pady= 20, padx=60, fill='both', expand=True)
        searchEntry = ctk.CTkEntry(master=search_screen_frame, placeholder_text='Enter title, author, or ISBN number to find books', width=280)
        #searchEntry.bind("<Return>")
        searchEntry.place(relx=0.5, rely=0.2, anchor='center')

        searchImg = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('search_img.jpg')), size=(24, 24))
        searchBtn = ctk.CTkLabel(search_screen_frame, image=searchImg, text='')
        bookImg = ctk.CTkLabel(search_screen_frame, text='this is here').place(relx= 0.45, rely = 0.7)
        #this searching through the database and 'returns' all titles associated with that piece of text
        #this text can be authors, title, or the isbn13
        def onSearchBtnClicked(event):
            print('this function was called')
            if searchEntry:
                search_text = searchEntry.get()
                with sqlite3.connect('book_list.db') as conn:
                    cursor = conn.cursor()
                    query = "SELECT * FROM book_registery WHERE LOWER(title) LIKE LOWER(?) OR LOWER(authors) LIKE ? OR isbn13 LIKE LOWER(?)"
                    params = (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%")
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
                        #here we have the current book selected as the first book in the list, duh
                        #i'm wanting to have the book cover of each book displayed and clickable to see more info on it
                        #also having some left and right arrow 'buttons' to travel through the collection of books
                        i = 0
                        curr_book = row[i]
                        #if left button is clicked, we go one to the left of the current book
                        #i-=1
                        #curr_book = row[i]

                        #if right button is clicked, we go one to the right of the current book
                        #i+=1
                        #curr_book = row[i]

        searchBtn.bind('<Button-1>', onSearchBtnClicked)
        searchBtn.place(relx=0.6, rely=0.2, anchor='center')

        #leftArrowBtn = ctk.CTkLabel()
        #rightArrowBtn = ctk.CTkLabel()

    #this is a simple method to just ease up the getting of images from images folder
    @staticmethod
    def getImg(file):
        img = os.path.join('..', 'images', fr'{file}')
        return img