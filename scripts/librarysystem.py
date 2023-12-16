import sqlite3
from PIL import Image
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
    def logout(self):
        pass

    #a search feature of available books, generes, authors, etc, etc.
    def search_books(self, title, author):
        pass

    #this removes a book from the inventory, could be either from borrowing, or librianan removing book from inventory
    def remove_book(self, book_id):
         pass

    #registers the account based on the username and password entered
    @staticmethod
    def register_user(username, password):
        user_exists = True
        with sqlite3.connect('user_accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM user_table WHERE username = ?", (username,))
            existing = cursor.fetchone()
            if not existing:
                user_exists = False

        if user_exists:
            ctkm(title='Registration Error', message='A username by that name already exists, try fixing your password', icon='warning', option_1='Close')
        else:
            with sqlite3.connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute("insert into user_table(username, password, role, books_borrowed) VALUES(?, ?, 'Member', 'None')", (username, User.hash_password(password)))
                conn.commit()
            ctkm(title='Registration Success', message='Account successfully registered', icon='check', option_1='Close')

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

        log_in_image = os.path.abspath(os.path.join('..', 'images', 'logingimage.jpg'))
        img = ctk.CTkImage(dark_image=Image.open(log_in_image), size=(400, 350))
        bg_label = ctk.CTkLabel(app, image=img, text='')
        bg_label.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(master=app, text='Login System')
        label.place(relx=0.5, rely=0.2, anchor='center')

        usernameEntry = ctk.CTkEntry(master=app, placeholder_text='Username')
        usernameEntry.place(relx=0.5, rely=0.3, anchor='center')
        passwordEntry = ctk.CTkEntry(master=app, show='*', placeholder_text='Password')
        passwordEntry.place(relx=0.5, rely=0.4, anchor='center')

        loginButton = ctk.CTkButton(master=app, text='Login',command=lambda: on_login_clicked(usernameEntry.get(), passwordEntry.get()), corner_radius=32).place(relx=0.5, rely=0.5, anchor='center')
        registerButton = ctk.CTkButton(master=app, text='Register',command=lambda: LibrarySystem.register_user(usernameEntry.get(), passwordEntry.get()), corner_radius=32).place(relx=0.5, rely=0.6, anchor='center')
        def onResize(event):
            new_size = (app.winfo_width(), app.winfo_height())
            img.configure(size=new_size)

        app.bind('<Configure>', onResize)
        app.mainloop()


    #use this function to make the retrival of images for the app much shorter and easeier so i dont have to write this code out a million times and loose my mind
    @staticmethod
    def get_img(img_path):
        #check if the image file exists
        if os.path.exists(img_path):
            #load the image using CTkImage
            img = ctk.CTkImage(dark_image=Image.open(img_path))
            return img
        #this is just here for debugging, might keep this in but idk, bc there's no way it shouldnt find the image, in theory, hopefully, please
        else:
            print(f"Image file not found: {img_path}")

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
        borrow_book_Btn = ctk.CTkButton(master=main_menu_frame, text='Borrow Books', command= lambda : onBorrowClicked, corner_radius=32).pack(pady=12, padx=10)
        return_book_Btn = ctk.CTkButton(main_menu_frame, text='Return Books', command= lambda : onReturnClicked, corner_radius=32).pack(pady=12, padx=10)
        def onSearchClicked():
            main_menu_frame.destroy()
            LibrarySystem.searchScreen()
        def onBorrowClicked():
            main_menu_frame.destroy()
            LibrarySystem.borrowBookScreen()

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

    #this will be a member only method/screen
    @staticmethod
    def borrowBookScreen():
        pass

    @staticmethod
    def returnBookScreen():
        pass

    # this will be a member only method/screen
    @staticmethod
    def registerScreen():
        pass

    #this will allow users to search the through the database of available books
    #have a progress bar to represent search progress
    @staticmethod
    def searchScreen():
        pass