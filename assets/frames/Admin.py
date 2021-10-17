from logging import ERROR
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import sqlite3

from assets import scripts

class Admin(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
######################################################################################
#   Search
        self.search = tk.StringVar()
        self.searchEntry = ttk.Entry(self, textvariable=self.search, style="TEntry", font=('Courier', 9, "bold"))
        self.searchEntry.place(relx=0.365, rely=0.08, anchor='center', width=530)
        self.search.set("Search Username")
        self.searchEntry.bind("<FocusIn>", self.deleteSearchPlaceholder)
        self.searchEntry.bind("<FocusOut>", self.addPlaceholder)

        self.searchButton = ttk.Button(self, text="Search", command=self.searchRecordInDatabase, style="Accent.TButton").place(relx=0.905, rely=0.08, anchor='center', width=100)
        self.searchButton = ttk.Button(self, text="Reset", command=self.resetRecordInDatabase, style="TButton").place(relx=0.77, rely=0.08, anchor='center', width=100)
######################################################################################
#   Treeview
        self.verticalScrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.verticalScrollbar.place(relx=.975, rely=.44, anchor="center", height=210)
        self.horizontalScrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.horizontalScrollbar.place(relx=.5, rely=.75, anchor="center", width=750)

        self.treeView = ttk.Treeview(self, show="headings", xscrollcommand=self.horizontalScrollbar.set , yscrollcommand = self.verticalScrollbar.set)
        self.treeView["columns"]=("id", "username","email", "password", "creation_date", "last_active", "admin_access")

        self.treeView.column('id', width=50, anchor="center")
        self.treeView.column('username', width=150, anchor="center")
        self.treeView.column('email', width=200, anchor="center")
        self.treeView.column('password', width=150, anchor="center")
        self.treeView.column('creation_date', width=150, anchor="center")
        self.treeView.column('last_active', width=150, anchor="center")
        self.treeView.column('admin_access', width=100, anchor="center")

        self.treeView.heading('id', text="ID", anchor="center")
        self.treeView.heading('username', text="Username", anchor="center")
        self.treeView.heading('password', text="Password", anchor="center")
        self.treeView.heading('email', text="Email", anchor="center")
        self.treeView.heading('creation_date', text="Creation Date", anchor="center")
        self.treeView.heading('last_active', text="Last Active", anchor="center")
        self.treeView.heading('admin_access', text="Admin Access?", anchor="center")

        self.treeView.place(relx=0.495,rely=0.44, anchor='center', width=750, height=210)
        self.verticalScrollbar.configure(command=self.treeView.yview)
        self.horizontalScrollbar.configure(command=self.treeView.xview)
######################################################################################
#   Buttons
        self.addButton = ttk.Button(self,command=self.addRecordInDatabase, text="Add", style="Accent.TButton")
        self.addButton.place(relx=0.2, rely=0.85, anchor='center', width=150)

        self.updateButton = ttk.Button(self,command=self.updateRecordInDatabase, text="Update", style="TButton")
        self.updateButton.place(relx=0.4, rely=0.85, anchor='center', width=150)
    
        self.deleteButton = ttk.Button(self,command=self.deleteRecordInDatabase, text="Delete", style="TButton")
        self.deleteButton.place(relx=0.6, rely=0.85, anchor='center', width=150)

        self.backButton = ttk.Button(self,command=lambda: self.master.loadframe("Home"), text="Back", style="TButton")
        self.backButton.place(relx=0.8, rely=0.85, anchor='center', width=150)
######################################################################################
#   Functions
    def deleteSearchPlaceholder(self, event):
        if self.search.get() == "Search Username":
            self.searchEntry.delete("0", "end")

    def addPlaceholder(self, event):
        if self.search.get() == "":
            self.searchEntry.insert("0", "Search Username")

    def searchRecordInDatabase(self):
        counter = 0
        self.treeView.delete(*self.treeView.get_children())
        self.master.cursor.execute("SELECT username, * FROM accounts WHERE username like ?", (self.search.get(),))
        databaseInfo = self.master.cursor.fetchall()
        for DBinfo in databaseInfo:
            DBinfoExtract = []
            for item in DBinfo:
                DBinfoExtract.append(item)
            self.treeView.insert(parent="",index=counter, iid=counter, text="", values=(DBinfoExtract[1], DBinfoExtract[2],DBinfoExtract[3],DBinfoExtract[4],DBinfoExtract[5],DBinfoExtract[6], DBinfoExtract[7]))
            counter = counter + 1

    def addRecordInDatabase(self):
        try:
            username, email, password = scripts.Messagebox(self, title="Create Account", message="").askdetails(username="Enter Username", email="Enter Email", password="Enter Password")
        except TypeError:
            return
        try:
            self.master.cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", (self.master.generateRandomString(5), username, email, password, self.master.getTime(), None, "N"))
            self.master.databaseConnection.commit()
            self.resetRecordInDatabase()
        except sqlite3.IntegrityError:
            self.addRecordInDatabase()

    def updateRecordInDatabase(self):
        currentlySelected = self.treeView.focus()
        currentData = (self.treeView.item(currentlySelected)["values"])
        if currentData == "":
            return
        try:
            username, email, password = scripts.Messagebox(self, title="Update Account", message="").askdetails(username=currentData[1], email=currentData[2], password=currentData[3])
        except TypeError:
            return
        self.master.cursor.execute("UPDATE accounts SET username = ?, email = ?, password = ? WHERE id = ?", (username, email, password, currentData[0]))
        self.master.databaseConnection.commit()
        values = self.treeView.item(currentlySelected, text="", values=(currentData[0], username, email, password, currentData[4], currentData[5], currentData[6]))

    def resetRecordInDatabase(self):
        self.treeView.delete(*self.treeView.get_children())
        self.load()

    def deleteRecordInDatabase(self):
        currentlySelected = self.treeView.focus()
        deleteData = (self.treeView.item(currentlySelected)["values"])
        self.master.cursor.execute("DELETE from accounts where username = ? AND email = ?", (deleteData[1], deleteData[2]))
        self.master.databaseConnection.commit()
        self.master.log.info(" User " + deleteData[1] + "'s data has been removed from the Database by " + self.master.user.get())
        currentSelectionDeletion = self.treeView.selection()[0]
        self.treeView.delete(currentSelectionDeletion)

    def load(self):
        counter = 0
        self.master.cursor.execute("SELECT * FROM accounts")
        databaseInfo = self.master.cursor.fetchall()
        for DBinfo in databaseInfo:
            DBinfoExtract = []
            for item in DBinfo:
                DBinfoExtract.append(item)
            self.treeView.insert(parent="",index=counter, iid=counter, text="", values=(DBinfoExtract[0],DBinfoExtract[1],DBinfoExtract[2],DBinfoExtract[3],DBinfoExtract[4],DBinfoExtract[5], DBinfoExtract[6]))
            counter = counter + 1
    
    def unload(self):
        self.treeView.delete(*self.treeView.get_children())
######################################################################################