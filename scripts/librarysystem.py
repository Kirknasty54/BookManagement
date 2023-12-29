import requests
import sqlite3
import webbrowser
from PIL import Image, ImageTk
from book import Book
import user as user
from tkinter import PhotoImage
from urllib.request import urlopen
import os
import customtkinter as ctk
from user import User
from CTkMessagebox import CTkMessagebox as ctkm
#from urlLabel import CTkUrlLabel

# set our colors/modes, title of the application and default size on launch
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title('The Library of Kirkandria')
app.after(0, lambda : app.state('zoomed'))
icon = PhotoImage(file=os.path.join('..', 'images', 'icon.png'))
app.wm_iconbitmap()
app.iconphoto(False, icon)


#this handles most of the logic of the overall app, split some of the functions to the classes i found appropriate 
class LibrarySystem:

    #this removes a book from the inventory, could be either from borrowing, or librianan removing book from inventory
    def remove_book(self, book_id):
         pass

    def borrow_book(self, username, book_id):
        pass

    def return_book(self, username, book_id):
        pass

    #this is the first screen that appears upon startup and handles the log in logic
    #depending on the log in entered, the user will either go to the member main menu screen or the librianian main menu screen, both screens have some differing options and some of the same
    @staticmethod
    def loginScreen():
        def onLoginClicked(username, password):
            can_login = User.loginCheck(username, password)
            if can_login == 0:
                for child in list(app.children.values()):
                    child.destroy()
                curr_user = User.getCurrUser(username, password)
                logged_user = User(username=curr_user['username'],
                                  password=curr_user['password'],
                                  role=curr_user['role'],
                                  borrowed_books=['books_borrowed'])
                if(logged_user.get_role() == 'Member'):LibrarySystem.mainMenuMemberScreen()

        img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('logingimage.jpg')), size=(400, 350))
        bg_label = ctk.CTkLabel(app, image=img, text='')
        bg_label.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(master=app, text='Login System')
        label.place(relx=0.5, rely=0.2, anchor='center')

        username_entry = ctk.CTkEntry(master=app, placeholder_text='Username')
        username_entry.place(relx=0.5, rely=0.3, anchor='center')
        password_entry = ctk.CTkEntry(master=app, show='*', placeholder_text='Password')
        password_entry.place(relx=0.5, rely=0.4, anchor='center')

        login_btn = ctk.CTkButton(master=app, text='Login',command=lambda: onLoginClicked(username_entry.get(), password_entry.get()), corner_radius=32).place(relx=0.5, rely=0.5, anchor='center')
        register_btn = ctk.CTkButton(master=app, text='Register',command=lambda: User.registerUser(username_entry.get(), password_entry.get()), corner_radius=32).place(relx=0.5, rely=0.6, anchor='center')
        gitHub_btn = ctk.CTkButton(master=app, text='GitHub', command=lambda : webbrowser.open_new('https://github.com/Kirknasty54'), width=10, height=10).place(relx=0.0, rely=0.0)
        #websiteBtn = ctk.CTkButton(master=app, text='Website', command=lambda : webbrowser.open_new(''),width=10, height=10).place(relx=0.0, rely=0.1)

        def onResize(event):
            new_size = (app.winfo_width(), app.winfo_height())
            img.configure(size=new_size)

        #app.bind('<Configure>', onResize)
        app.mainloop()

    #this is the main menu screen for members only, gives them a variety of options like searching for books, borrowing books, returning books, and log out
    #might eventually add a recommendation system based on previously borrowed books
    @staticmethod
    def mainMenuMemberScreen():
        main_menu_frame = ctk.CTkFrame(master=app)
        main_menu_frame.pack(pady=20, padx=60, fill='both', expand=True)
        label = ctk.CTkLabel(master=main_menu_frame, text='Main Menu\nWelcome Member')
        label.pack(pady=12, padx=10)
        search_book_btn = ctk.CTkButton(master=main_menu_frame, text='Search for Books', command= lambda : onSearchClicked(), corner_radius=32).pack(pady=12, padx=10)
        return_book_btn = ctk.CTkButton(main_menu_frame, text='Return Books', command= lambda : onReturnClicked(), corner_radius=32).pack(pady=12, padx=10)
        logout_btn = ctk.CTkButton(main_menu_frame, text='Logout', command= lambda: User.logout(main_menu_frame), corner_radius=32).pack(pady=12, padx=10)

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
        search_entry = ctk.CTkEntry(master=search_screen_frame, placeholder_text='Enter title, author, or ISBN number to find books', width=280)
        #search_entry.bind("<Return>")
        search_entry.place(relx=0.5, rely=0.2, anchor='center')
        #book_img = CTkUrlLabel()

        search_img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('search_img.jpg')), size=(24, 24))
        search_btn = ctk.CTkLabel(search_screen_frame, image=search_img, text='')
        #this searching through the database and 'returns' all titles associated with that piece of text
        #this text can be authors, title, or the isbn13
        def onSearchBtnClicked(event):
            print('this function was called')
            if search_entry:
                search_text = search_entry.get()
                with sqlite3.connect('book_list.db') as conn:
                    cursor = conn.cursor()
                    sql_query = f"SELECT * FROM book_registery WHERE title LIKE '%{search_text}%' OR authors LIKE '%{search_text}%' OR isbn13 LIKE '%{search_text}%'"
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    for row in rows:
                        book_cover = Book.getImgUrl(search_screen_frame, row[6]).place(relx=0.6, rely=0.6, anchor='center')
                        print(row[6])
                        break

        search_btn.bind('<Button-1>', onSearchBtnClicked)
        search_btn.place(relx=0.6, rely=0.2, anchor='center')
        #left_arrow_btn = ctk.CTkLabel()
        #right_arrow_btn = ctk.CTkLabel()

    #this is a simple method to just ease up the getting of images from images folder
    @staticmethod
    def getImg(file):
        img = os.path.join('..', 'images', fr'{file}')
        return img