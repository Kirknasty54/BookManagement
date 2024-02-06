import pickle
import requests
from threading import Thread
import sqlite3
import webbrowser
from PIL import Image, ImageTk
from book import Book
import user as user
from tkinter import PhotoImage
import os
import customtkinter as ctk
from user import User
from CTkMessagebox import CTkMessagebox as ctkm
from urlLabel import CTkUrlLabel
from textwrap import wrap
from CTkListbox import *

# set our colors/modes, title of the application and default size on launch
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title('The Library of Kirkandria')
app.resizable(False, False)
app.after(0, lambda : app.state('zoomed'))
icon = PhotoImage(file=os.path.join('..', 'images', 'icon.png'))
app.wm_iconbitmap()
app.iconphoto(False, icon)
u_id = 0

#this handles most of the logic of the overall app, split some of the functions to the classes i found appropriate
class LibrarySystem:

    #this is the first screen that appears upon startup and handles the log in logic
    #depending on the log in entered, the user will either go to the member main menu screen or the librianian main menu screen, both screens have some differing options and some of the same
    @staticmethod
    def loginScreen():
        def onLoginClicked(username, password):
            can_login = User.loginCheck(username, password)
            if can_login == 0:
                app.unbind('<Configure>')
                for child in list(app.children.values()): child.destroy()
                curr_user = User.getCurrUser(username, password)

                logged_user = User(username=curr_user['username'],
                                  password=curr_user['password'],
                                  role=curr_user['role'],
                                  id =['id'])
                if(logged_user.get_role() == 'Member'):LibrarySystem.mainMenuMemberScreen()
                global u_id
                u_id = logged_user.get_curr_id(username, password)

        img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('logingimage.jpg')), size=(400, 350))
        bg_label = ctk.CTkLabel(app, image=img, text='')
        bg_label.pack()

        login_frame = ctk.CTkFrame(master=bg_label, width=320, height=360, corner_radius=20)
        login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        label = ctk.CTkLabel(master=login_frame, text='Login', font=ctk.CTkFont(weight="bold", size=20))
        label.place(x=login_frame._current_width/2 -25,y=50)
        username_entry = ctk.CTkEntry(master=login_frame, placeholder_text='Username')
        username_entry.place(x=login_frame._current_width/2 -70, y =110)
        password_entry = ctk.CTkEntry(master=login_frame, show='*', placeholder_text='Password')
        password_entry.place(x=login_frame._current_width/2 -70, y =165)
        '''forgot_password_link = ctk.CTkLabel(master=login_frame, text='Forgot Password?', cursor='hand2', text_color='blue', font=ctk.CTkFont())
        forgot_password_link.bind("<Button-1>", )
        forgot_password_link.place(x=login_frame._current_width/2 -50, y =200)'''

        login_btn = ctk.CTkButton(master=login_frame, text='Login',command=lambda: onLoginClicked(username_entry.get(), password_entry.get())).place(x=login_frame._current_width/2 -70, y =240)
        register_btn = ctk.CTkButton(master=login_frame, text='Register',command=lambda: User.registerUser(username_entry.get(), password_entry.get())).place(x=login_frame._current_width/2 -70, y =290)
        gitHub_btn = ctk.CTkButton(master=app, text='GitHub', command=lambda : webbrowser.open_new('https://github.com/Kirknasty54'), width=10, height=10).place(relx=0.0, rely=0.0)
        #websiteBtn = ctk.CTkButton(master=app, text='Website', command=lambda : webbrowser.open_new(''),width=10, height=10).place(relx=0.0, rely=0.1)

        #this serves to resize the background image whenever the window size of the app is changed, avoids any jank
        def onResize(event):
            new_size = (app.winfo_width(), app.winfo_height())
            img.configure(size=new_size)
        app.bind('<Configure>', onResize)
        app.mainloop()

    # returns to the appropiate screen based on the case based into the function
    # want to return to search screen if were hitting the back arrow on the book screen, and thenn return to the main menu screen if we press search screen back arrow
    def onBackArrowBtnClicked(case):
        match case:
            case 0:
                for child in list(app.children.values()): child.destroy()
                LibrarySystem.mainMenuMemberScreen()
            case 1:
                for child in list(app.children.values()): child.destroy()
                LibrarySystem.searchScreen()

    #this is the main menu screen for members only, gives them a variety of options like searching for books, borrowing books, returning books, and log out
    #might eventually add a recommendation system based on previously borrowed books
    @staticmethod
    def mainMenuMemberScreen():
        main_menu_frame = ctk.CTkFrame(master=app)
        main_menu_frame.pack(pady=20, padx=60, fill='both', expand=True)
        label = ctk.CTkLabel(master=main_menu_frame, text='Main Menu\nWelcome Member', font=(None, 35))
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

    @staticmethod
    def returnBookScreen():
        return_frame = ctk.CTkFrame(master=app)
        left_img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('left_arrow.png')), size=(25, 25))
        label = ctk.CTkLabel(master=return_frame, text='Return Menu', font=(None, 35))
        back_arrow = ctk.CTkButton(master=return_frame, image=left_img, fg_color='transparent',
                                   hover=False, text='', command=lambda: LibrarySystem.onBackArrowBtnClicked(0), width=10, height=10)
        label.pack(anchor=ctk.CENTER, side=ctk.TOP)
        books_to_return = ctk.CTkComboBox(master = return_frame, width=400, state='readonly')
        books_to_return.set('Select a book to return')
        with(sqlite3.connect('user_accounts.db')) as conn:
            cursor = conn.cursor()
            sql_query = "SELECT book from book_transaction where user_id = ? and state = ?"
            cursor.execute(sql_query, (u_id, 'borrowed',))
            results = cursor.fetchall()
            normalized_results = [result[0].strip("'") for result in results]
            books_to_return.configure(values=normalized_results)

        return_btn = ctk.CTkButton(master=return_frame, text='Return', command=lambda: return_book())

        return_frame.pack(pady=20, padx=60, fill='both', expand=True)
        books_to_return.pack(anchor=ctk.CENTER, side=ctk.TOP, pady=0)
        back_arrow.pack(side=ctk.TOP, anchor=ctk.NW)
        return_btn.pack(anchor=ctk.CENTER, side=ctk.TOP)

        def return_book():
            selected_return = books_to_return.get()
            with(sqlite3.connect('user_accounts.db')) as conn:
                cursor = conn.cursor()
                #sql_query_insert = "INSERT INTO book_transaction (user_id, book, state) VALUES (?, ?, ?)"
                #sql_query_update_quantity = "UPDATE book_registery SET quantity = quantity-1 WHERE title = ?"
                sql_query_update = "UPDATE book_transaction SET state = 'returned' WHERE book = ? AND user_id = ?"
                cursor.execute(sql_query_update, (selected_return, u_id))
                conn.commit()
                app.update()
                books_to_return.update()


    #this will allow users to search the through the database of available books
    #might have a progress bar to represent search progress
    @staticmethod
    def searchScreen():
        search_frame = ctk.CTkFrame(master=app)
        search_frame.pack(pady=20, padx=60, fill='both', expand=True)
        search_entry = ctk.CTkEntry(master=search_frame, placeholder_text='Enter title, author, or ISBN number to find books', width=280)
        search_entry.place(x=search_frame._current_width/2 +450, y=20)
        search_img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('search_img.png')), size=(25, 25))
        search_btn = ctk.CTkButton(master=search_frame, image=search_img, fg_color="transparent",
                                   hover=False, text='', command = lambda : onSearchBtnClicked(), width=10, height=20)
        app.update()
        search_btn.place(x=search_entry.winfo_x()+142, y=18)
        right_img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('right_arrow.png')), size =(25, 25))
        left_img = ctk.CTkImage(dark_image=Image.open(LibrarySystem.getImg('left_arrow.png')), size=(25, 25))
        book_cover = CTkUrlLabel(master=search_frame)
        book_desc = ctk.CTkLabel(master=search_frame)
        back_arrow = ctk.CTkButton(master=search_frame, image=left_img, fg_color='transparent',
                                   hover=False, text='', command = lambda : LibrarySystem.onBackArrowBtnClicked(0), width=10, height=10)
        back_arrow.pack(side=ctk.TOP, anchor=ctk.NW)

        #this searches through the database and 'returns' all titles associated with that piece of text
        #this text can be authors, title, or the isbn13
        idx=0
        books_found = []
        def onSearchBtnClicked():
            def search():
                if search_entry.get():
                    search_text = search_entry.get()
                    with sqlite3.connect('book_list.db') as conn:
                        cursor = conn.cursor()
                        sql_query = f"SELECT * FROM book_registery WHERE title LIKE '%{search_text}%' OR authors LIKE '%{search_text}%' OR isbn13 LIKE '%{search_text}%'"
                        cursor.execute(sql_query)
                        nonlocal books_found
                        books_found = cursor.fetchall()
                        if books_found:
                            book_cover.configure(url=Book.getImgUrl(books_found[0][6]), text='', cursor="hand2", url_image_size=(300, 300))
                            book_cover.place(x=search_frame._current_width/2 -150, y=search_frame._current_height/2 -200)
                            book_cover.bind("<Button-1>", onBookClicked)
                            right_btn = ctk.CTkButton(master=search_frame, image=right_img, command=lambda: rightBtnClicked(books_found, book_cover, book_desc),
                                                      text='',fg_color="transparent", width=10, height=20).place(x=search_frame._current_width/2 +150, y = search_frame._current_height/2 -60)
                            left_btn = ctk.CTkButton(master=search_frame, image=left_img, command=lambda: leftBtnClicked(books_found, book_cover, book_desc),
                                                     text='', fg_color="transparent", width=10, height=20).place(x=search_frame._current_width/2 -190, y=search_frame._current_height/2 -60)
                            book_desc.configure(text=books_found[0][5][0:50]+'\n'+books_found[0][5][50:100])
                            book_desc.place(x=search_frame._current_width/2-150, y = search_frame._current_height/2+125)

                        else: ctkm(title='No Such Book Found', message='Looks like we don\'t have any matching books. Try again or let a librarian know.',
                                icon='warning', option_1='Close')
                else:ctkm(title='Enter Something', message='Looks like you forgot to enter in anything',
                          icon='warning', option_1='Close')
            #use threading to help prevent gui lag
            Thread(target=search).start()

        #this moves to the right and if we reach the end of the list, simply reset to the beginning to avoid any list range error bs
        def rightBtnClicked(books_found, book_cover, book_desc):
            nonlocal idx
            idx += 1
            if(idx >= len(books_found)):
                idx = 0
            book_cover.configure(url=Book.getImgUrl(books_found[idx][6]))
            book_desc.configure(text=books_found[idx][5][0:50]+'\n'+books_found[idx][5][50:100])

        #this moves to the left and if we reach the 'left-most' point of the list, we simply move to the beginning of the list
        def leftBtnClicked(books_found, book_cover, book_desc):
            nonlocal idx
            idx -= 1
            if(idx <= -len(books_found)):
                idx = 0
            book_cover.configure(url=Book.getImgUrl(books_found[idx][6]))
            book_desc.configure(text=books_found[idx][5][0:50]+'\n'+books_found[idx][5][50:100])

        #this takes the user to a main page for the book they clicked on, has some more info about the book like the author, publisher, publication date
        #also gives the user the option to borrow if they are a member and not a librarian
        #will let the user know if there are no more copies of the book available
        #if no copies available then prevent user from attempting to borrow book
        def onBookClicked(event):
            for child in list(app.children.values()): child.destroy()
            book_frame = ctk.CTkFrame(master=app)
            book_frame.pack(pady=20, padx=60, fill='both', expand=True)
            back_arrow = ctk.CTkButton(master=book_frame, image=left_img, fg_color='transparent',
                                       hover=False, text='', command=lambda: LibrarySystem.onBackArrowBtnClicked(1), width=10,
                                       height=10)
            back_arrow.pack(side=ctk.TOP, anchor=ctk.NW)

            book_borrow_cover = CTkUrlLabel(master=book_frame)
            book_borrow_title = ctk.CTkLabel(master=book_frame)
            book_borrow_desc = ctk.CTkLabel(master=book_frame)
            book_publisher = ctk.CTkLabel(master=book_frame)
            book_publication_date = ctk.CTkLabel(master=book_frame)
            book_isbn13 = ctk.CTkLabel(master=book_frame)
            book_quantity = ctk.CTkLabel(master=book_frame)
            book_borrow_button = ctk.CTkButton(master=book_frame)

            book_borrow_cover.configure(url=Book.getImgUrl(books_found[idx][6]), text='',
                                 url_image_size=(300, 300))
            s = wrap(books_found[idx][5], 100)
            book_borrow_title.configure(text='Title: ' + books_found[idx][1])
            book_borrow_desc.configure(text='Book Desc: ' + '\n'.join(s))
            book_publisher.configure(text='Publisher: ' + books_found[idx][3])
            book_publication_date.configure(text='Publication Date:' + books_found[idx][4])
            book_isbn13.configure(text='ISBN-13 Number: ' + books_found[idx][6])
            book_quantity.configure(text='Number in stock: ' + str(books_found[idx][7]))
            book_borrow_button.configure(text='Borrow Book', command=lambda:on_borrow_clicked(books_found[idx][1], book_quantity))

            book_borrow_cover.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_borrow_title.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_borrow_desc.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_publisher.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_publication_date.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_isbn13.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_quantity.pack(anchor=ctk.CENTER, side=ctk.TOP)
            book_borrow_button.pack(anchor=ctk.CENTER, side=ctk.TOP)

        #this handles the actual borrowing logic, checking to see if the current user already has the book
        #if they do, then prevent them from borrowing again
        #also see if there is a valid quantity of books, if not, then alert user and prevent them from borrowing
        def on_borrow_clicked(book_title, book_quantity):
            acknowledgement = ctkm(title='Borrow Book', message='Are you sure you want to borrow this book?', icon='check', option_1='No', option_2='Yes')
            if acknowledgement.get() == 'Yes':
                with sqlite3.connect('user_accounts.db') as conn:
                    cursor = conn.cursor()
                    sql_query = f"SELECT book FROM book_transaction WHERE user_id = ? and state = ?"
                    cursor.execute(sql_query, (u_id, 'borrowed',))
                    results = cursor.fetchall()
                    normalized_results = [result[0].strip("'") for result in results]
                    if book_title not in normalized_results:
                        qty = 0
                        with sqlite3.connect('book_list.db') as conn2:
                            cursor2 = conn2.cursor()
                            sql_get_qty = "SELECT quantity FROM book_registery WHERE title = ?"
                            cursor2.execute(sql_get_qty, (book_title,))
                            qty = cursor2.fetchone()[0]
                            if qty <= 0:
                                ctkm(title='Not enough books',
                                     message='Looks like we dont have any of those books in stock, try again later',
                                     icon='warning', option_1='Close')
                            else:
                                sql_query_insert= "INSERT INTO book_transaction (user_id, book, state) VALUES (?, ?, ?)"
                                cursor.execute(sql_query_insert, (u_id, book_title, 'borrowed'))
                                conn.commit()
                                sql_query_update_quantity = "UPDATE book_registery SET quantity = quantity-1 WHERE title = ?"
                                cursor2.execute(sql_query_update_quantity, (book_title,))
                                book_quantity.configure(text='Number in stock: ' + str(qty-1))
                                conn2.commit()
                    else:
                        ctkm(title='Already Borrowed', message='Looks like you\'re already borrowing this book',
                             icon='warning', option_1='Close')

    #this is a simple method to just ease up the getting of images from images folder
    #could have downloaded all book cover images from google api, might be slightly faster to display image, but i really dont want this to take up that much space
    #also just like my current method a lot better
    @staticmethod
    def getImg(file):
        img = os.path.join('..', 'images', fr'{file}')
        return img