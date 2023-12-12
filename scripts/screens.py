import customtkinter as ctk
import book as book
import user as user
import librarysystem as ls
import os
import tkinter as tk

def loginScreen():
    #set our colors/modes, title of the application and default size on launch
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    app.title('The Library of Kirkandria')
    app.geometry("500x350")

    #create a loginFrame that we will insert our prompts for username and password, and buttons for either logging in or registering
    loginFrame = ctk.CTkFrame(master=app)
    loginImg = ctk.CTkImage(master=loginFrame, image=os.path.join('../scripts', 'loginimg.jpg')).pack(side='left')

    loginFrame.pack(pady=20, padx=60, fill='both', expand=True)

    label = ctk.CTkLabel(master=loginFrame, text='Login System')
    label.pack(pady=12, padx=10)

    usernameEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Username')
    passwordEntry = ctk.CTkEntry(master=loginFrame, placeholder_text='Password')
    usernameEntry.pack(pady=12, padx=10)
    passwordEntry.pack(pady=12, padx=10)

    loginButton = ctk.CTkButton(master=loginFrame, text='Login')
    registerButton = ctk.CTkButton(master=loginFrame, text='Register')

    loginButton.pack(pady=12, padx=10)
    registerButton.pack(pady=12, padx=10)
    app.mainloop()

def mainmenuScreen():
    pass

def addBookScreen():
    pass

def removeBookScreen():
    pass

def borrowBookScreen():
    pass

def registerScreen():
    pass

def searchScreen():
    pass