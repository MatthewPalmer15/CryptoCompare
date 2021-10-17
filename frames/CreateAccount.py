from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import os
import datetime
import sqlite3

class CreateAccount(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
######################################################################################
#   Username Entry
        self.username = tk.StringVar()
        self.username.trace('w', self.usernameLimit)     
        self.usernameEntry = ttk.Entry(self, textvariable=self.username, style="TEntry", font=('Courier', 9, "bold"))
        self.usernameEntry.place(relx=.5,rely=.18, anchor="center", width=500, height=40)
        self.usernameEntry.bind("<FocusIn>", self.deleteUsernamePlaceholder)
        self.usernameEntry.bind("<FocusOut>", self.addPlaceholder)

        self.email = tk.StringVar()
        self.email.set("Email")
        self.emailEntry = ttk.Entry(self, textvariable=self.email, style="TEntry", font=('Courier', 9, "bold"))
        self.emailEntry.place(relx=0.375, rely=0.3, anchor='center', width=300)
        self.emailEntry.bind("<FocusIn>", lambda event: self.emailEntry.delete("0", "end"))
        self.emailEntry.bind("<FocusOut>", self.addPlaceholder)

        self.emailSuffix = ["@gmail.com","@googlemail.com", "@outlook.com", "@yahoo.co.uk"]
        self.emailSuffix = sorted(self.emailSuffix)
        self.emailSuffixChoice = tk.StringVar()
        self.emailSuffixBox = ttk.OptionMenu(self, self.emailSuffixChoice, self.emailSuffix[0], *self.emailSuffix, style="TOptionMenu").place(relx=0.692, rely=0.3, anchor='center', width=190)
        self.emailSuffixChoice.set(self.emailSuffix[0])

        self.password = tk.StringVar()   
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, style="TEntry", font=('Courier', 9, "bold"))
        self.passwordEntry.place(relx=.5,rely=.42, anchor="center", width=500, height=40)
        self.passwordEntry.bind("<FocusIn>", self.deletePasswordPlaceholder)
        self.passwordEntry.bind("<FocusOut>", self.addPlaceholder)

        self.confirmPassword = tk.StringVar()   
        self.confirmPasswordEntry = ttk.Entry(self, textvariable=self.confirmPassword, style="TEntry", font=('Courier', 9, "bold"))
        self.confirmPasswordEntry.place(relx=.5,rely=.55, anchor="center", width=500, height=40)
        self.confirmPasswordEntry.bind("<FocusIn>", self.deleteConfirmPasswordPlaceholder)
        self.confirmPasswordEntry.bind("<FocusOut>", self.addPlaceholder)
######################################################################################
#   Buttons
        self.createAccountButton = ttk.Button(self, command=self.createAccount, text="Create Account", style="Accent.TButton")
        self.createAccountButton.place(relx=0.3, rely=0.8, anchor='center', width=300)

        self.backButton = ttk.Button(self,command=lambda: self.master.loadframe("Home"), text="Back", style="TButton")
        self.backButton.place(relx=0.7, rely=0.8, anchor='center', width=300)
######################################################################################
#   Functions
    def usernameLimit(self, *args):
        value = self.username.get()
        if len(value) > 25: 
            self.username.set(value[:25])

    def addPlaceholder(self, event):
        if self.username.get() == "":   
            self.usernameEntry.insert("0", "Username")
        if self.email.get() == "":
            self.emailEntry.insert("0", "Email")
        if self.password.get() == "":
            self.passwordEntry.configure(show="")
            self.passwordEntry.insert("0", "Password")
        if self.confirmPassword.get() == "":
            self.confirmPasswordEntry.configure(show="")
            self.confirmPasswordEntry.insert("0", "Confirm Password")
    
    def deleteUsernamePlaceholder(self, event):
        if self.username.get() == "Enter Username":
            self.usernameEntry.delete("0", "end")

    def deletePasswordPlaceholder(self, event):
        if self.password.get() == "Enter Password":
            self.passwordEntry.delete("0", "end")
            self.passwordEntry.configure(show="*")

    def deleteConfirmPasswordPlaceholder(self, event):
        self.confirmPasswordEntry.delete("0", "end")
        self.confirmPasswordEntry.configure(show="*")

    def createAccount(self):
        username = self.username.get().lower()
        email = (self.email.get() + self.emailSuffixChoice.get()).lower()
        if len(self.username.get()) < 5 or self.username.get() == "Enter Username":
            tkinter.messagebox.showerror("Invalid Username", "The Username must be above 5 characters")
        elif len(self.password.get()) < 5 or self.password.get() == "Enter Password":
            tkinter.messagebox.showerror("Invalid Password", "The Password must be above 5 characters")
        elif self.password.get() != self.confirmPassword.get():
            tkinter.messagebox.showerror("Re-enter Password", "Your Password does not match")
        else:
            try:
                self.master.cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", (self.master.generateRandomString(5), username, email, self.password.get(), self.master.getTime(), None, "N"))
                self.master.databaseConnection.commit()
                tkinter.messagebox.showinfo("Welcome!", "Your Account has now been Activated!")
                self.master.loadframe("Home")
            except Exception as Error:
                self.master.log.error(Error)
                tkinter.messagebox.showerror("Lost Connection", "The Database cannot be accessed at this time")

    def load(self):
        self.username.set("Enter Username")
        self.email.set("Enter Email")
        self.emailSuffixChoice.set(self.emailSuffix[0])
        self.password.set("Enter Password")
        self.confirmPassword.set("Confirm Password")
        self.passwordEntry.configure(show="")
        self.confirmPasswordEntry.configure(show="")
        ######################################################################################