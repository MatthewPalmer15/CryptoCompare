from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import os
import datetime
import sqlite3

class Home(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
######################################################################################
#   Username Entry
        self.username = tk.StringVar()
        self.username.set("Enter Username")
        self.username.trace('w', self.usernameLimit)  
        self.usernameEntry = ttk.Entry(self, textvariable=self.username, style="TEntry", font=('Courier', 9, "bold"))
        self.usernameEntry.place(relx=.5,rely=.35, anchor="center", width=500, height=40)
        self.usernameEntry.bind("<FocusIn>", self.deleteUsernamePlaceholder)
        self.usernameEntry.bind("<FocusOut>", self.addPlaceholder)

        self.password = tk.StringVar()   
        self.password.set("Enter Password")
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, style="TEntry", font=('Courier', 9, "bold"))
        self.passwordEntry.place(relx=.5,rely=.5, anchor="center", width=500, height=40)
        self.passwordEntry.bind("<FocusIn>", self.deletePasswordPlaceholder)
        self.passwordEntry.bind("<FocusOut>", self.addPlaceholder)

######################################################################################
#   Buttons
        self.logInButton = ttk.Button(self, command=self.logIn, text="Log In", style="Accent.TButton")
        self.logInButton.place(relx=0.3, rely=0.8, anchor='center', width=300)

        self.signUpButton = ttk.Button(self,command=lambda: self.master.loadframe("CreateAccount"), text="Sign Up", style="TButton")
        self.signUpButton.place(relx=0.7, rely=0.8, anchor='center', width=300)
######################################################################################
#   Functions
    def usernameLimit(self, *args):
        value = self.username.get()
        if len(value) > 25: 
            self.username.set(value[:25])

    def addPlaceholder(self, event):
        if self.username.get() == "":   
            self.usernameEntry.insert("0", "Enter Username")
        if self.password.get() == "":
            self.passwordEntry.configure(show="")
            self.passwordEntry.insert("0", "Enter Password")
    
    def deleteUsernamePlaceholder(self, event):
        if self.username.get() == "Enter Username":
            self.usernameEntry.delete("0", "end")

    def deletePasswordPlaceholder(self, event):
        if self.password.get() == "Enter Password":
            self.passwordEntry.delete("0", "end")
            self.passwordEntry.configure(show="*")

    def logIn(self):
        self.master.loadframe("Dashboard")

def load(self):
        self.username.set("Enter Username")
        self.password.set("Enter Password")
        self.passwordEntry.configure(show="")
        ######################################################################################
