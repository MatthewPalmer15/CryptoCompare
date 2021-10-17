import tkinter as tk
from tkinter import ttk
import os
import logging
import datetime
import logging
import sqlite3
import random
import string

from assets import frames
from assets import scripts

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x400')
        self.resizable(False, False)
        self.title("CryptoCompare")
        self.tk.call('source', 'assets/theme/sun-valley.tcl')
        self.tk.call('set_theme', 'dark')
        self.style = scripts.Style(self)
        self.configure()
        
        self.databaseConnection = sqlite3.connect("assets/database/database.db")
        self.cursor = self.databaseConnection.cursor()

        self.setupDatabaseLogger(loglevel=logging.INFO) 
        self.titlebar = scripts.Titlebar(self)
        self.titlebar.pack(side="top", fill="x")

        self.user = tk.StringVar()
        self.updating = False
        self.shownFrame = None
        self.lastFrame = None
        self.allFrames = self.create_frames()
        self.loadframe('Home')

    def create_frames(self):
        allFrames = {}
        for filename in os.listdir('Assets/frames/'):
            if (filename.startswith('_')):
                continue
            
            frameName = filename.replace('.py', '')
            allFrames[frameName] = eval(f'frames.{frameName}(self)')
        return allFrames
        
        
    def loadframe(self, frameName:str):
        self.lastFrame = self.shownFrame.__class__.__name__
        try:
            self.shownFrame.pack_forget()
            self.shownFrame.unload()
        except AttributeError:
            pass
        
        self.shownFrame = self.allFrames[frameName]
        self.shownFrame.pack(fill='both', expand=True)

        try:
            self.shownFrame.load()
        except AttributeError:
            pass

    def getTheme(self):
        return str(self.tk.call("ttk::style", "theme", "use")).split("-")[-1]

    def onThemeChange(self, button, num1, num2):
        image = tk.PhotoImage(file =f"assets/images/user_profile_{self.getTheme()}.png")
        image = image.subsample(num1, num2)
        button.configure(image=image)
        button.image=image
        self.titlebar.configure_style()

    def setupDatabaseLogger(self, loglevel):
        LOG_FORMAT = "%(levelname)s | %(asctime)s | Reason: %(message)s"
        logging.basicConfig(filename="assets/database/database_log.txt", filemode='a', format=LOG_FORMAT, datefmt="%d-%b-%y %H:%M:%S", level=loglevel)
        self.log = logging.getLogger()
    
    def getTime(self):
        getTimeDate = datetime.datetime.now()
        ACCOUNT_CREATED_TIME = getTimeDate.strftime("%d/%m/%Y %H:%M:%S")
        return ACCOUNT_CREATED_TIME

    def generateRandomString(self, size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size)).upper()


    def closeApplication(self):
        self.databaseConnection.close()
        exit()
        
if (__name__ == "__main__"):
    app = Application()
    app.mainloop()
