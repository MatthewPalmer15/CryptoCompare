from tkinter import ttk
import tkinter as tk
import tkinter
import tkinter.messagebox
import sqlite3

from assets import scripts

class Settings(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
######################################################################################
#   Button
        self.userProfileImage = ttk.Label(self, style="TLabel")
        self.userProfileImage.place(relx=.5, rely=.15, anchor="center")
        self.userProfileName = ttk.Label(self, textvariable=self.master.user, style="TLabel", font=('Courier', 11, "bold")).place(relx=.5, rely=.275, anchor="center")
######################################################################################
#   Label     
        self.adminButton = ttk.Button(self, text="Adminstrator Mode", command=self.admin, style='TButton').place(relx=0.5, rely=0.65, anchor='center', width=300)
        self.deleteAccountButton = ttk.Button(self, text="Delete Account", command=self.deleteAccount, style='TButton').place(relx=0.5, rely=0.775, anchor='center', width=300)
        self.backButton = ttk.Button(self, text="Back", command=self.back, style='TButton').place(relx=0.5, rely=0.9, anchor='center', width=300)
######################################################################################
#   Buttons
        getThemeValue = str(master.tk.call("ttk::style", "theme", "use")).split("-")[-1]
        self.theme = tk.StringVar(value=getThemeValue)
        self.theme.trace_add("write", lambda *_ : self.master.onThemeChange(self.userProfileImage, 2, 2))
        self.theme.trace_add("write", lambda *_ : master.tk.call("set_theme", self.theme.get()))

        darkMode = ttk.Checkbutton(self, text="Dark Mode ", compound="right", variable=self.theme, onvalue="dark", offvalue="light", style="Switch.TCheckbutton").place(relx=0.5,rely=0.4, anchor="center")
        lightMode = ttk.Checkbutton(self, text="Light Mode ", compound="right", variable=self.theme, onvalue="light", offvalue="dark", style="Switch.TCheckbutton").place(relx=0.5,rely=0.5, anchor="center")
######################################################################################
#   Functions
    def deleteAccount(self):
        if self.master.user.get() == "Guest":
            pass
        else:
            test = scripts.Messagebox(self, title="Hello", message="bruh").askyesno()
            if test is True:
                self.master.cursor.execute("DELETE FROM accounts WHERE username = ?", (self.master.user.get(),))
                self.master.loadframe("Home")
                self.master.databaseConnection.commit()

    def admin(self):
        #self.master.cursor.execute("SELECT * FROM accounts WHERE username = ? AND admin_access = ?", (self.master.user.get(), "Y"))
        #data = self.master.cursor.fetchall()
        #if len(data) == 0:
        #    tkinter.messagebox.showerror("Account Not Authorised", "Account does not meet the requirements to access Administrator Mode")
        #else:
        self.master.loadframe("Admin")



    def back(self):
        if self.master.lastFrame is None:
            return
        self.master.loadframe(self.master.lastFrame)

    def load(self):
        self.master.onThemeChange(self.userProfileImage, 2, 2)
######################################################################################