import tkinter as tk
from tkinter import ttk
from ctypes import windll
import cryptocompare
import matplotlib.pyplot as plt
import datetime
from PIL import Image, ImageTk

from assets import scripts


# Windows OS styles for custom taskbar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


IMAGE_PATH = "assets/images/"  # path to your images


class Messagebox(tk.Toplevel):
    def __init__(self, master, title:str, message:str, **kw):
        try: super().__init__(master, **kw)
        except RuntimeError: return
        
        self._title = title
        self._message = message
        self.returnValue = None

        # get root
        self.root = master        
        while (str(self.root) != '.'): 
            self.root = self.nametowidget(self.root.winfo_parent())
 
        # grab controlls and set window to top layer
        self.attributes("-topmost", True)
        self.transient(self.root)
        self.grab_set()
    
        self.setup_titlebar()
        self.setup_window()
        
        self.yesBtn = ttk.Button(self.buttons, text='Yes', style='Messagebox.TButton', takefocus=False, command=lambda:self._return(True))
        self.noBtn = ttk.Button(self.buttons, text='No', style='Messagebox.TButton', takefocus=False, command=lambda:self._return(False))
        self.okayBtn = ttk.Button(self.buttons, text='Ok', style='Messagebox.TButton', takefocus=False, command=lambda:self._return(True))
        self.cancelBtn = ttk.Button(self.buttons, text='Cancel', style='Messagebox.TButton', takefocus=False, command=lambda:self._return(None))
        
        self.graphDisplay = ttk.Label(self)

    def _return(self, value) -> None:
        self.returnValue = value
        self.close()
        
        
    def askyesno(self) -> bool:
        self.yesBtn.pack(side='right', ipady=3)
        self.noBtn.pack(side='right', padx=30, ipady=3, before=self.yesBtn)
        self.root.wait_window(self)
        return self.returnValue
    
        
    def askyescancel(self) -> bool:
        self.yesBtn.pack(side='right', ipady=3)
        self.cancelBtn.pack(side='right', padx=30, ipady=3, before=self.yesBtn)
        self.root.wait_window(self)
        return self.returnValue
        
        
    def showinfo(self) -> bool:
        self.okayBtn.pack(side='right', padx=30, ipady=3)
        self.root.wait_window(self)
        return self.returnValue
        
        
    def showwarning(self) -> bool:
        self.okayBtn.pack(side='right', padx=30, ipady=3)
        self.root.wait_window(self)
        return self.returnValue
        
        
    def showerror(self) -> bool:
        self.okayBtn.pack(side='right', padx=30, ipady=3)
        self.root.wait_window(self)
        return self.returnValue

    def userDetails(self):
        pass

    def showDailyGraph(self, cryptocurrency, currency):
        self.geometry("360x360")
        self.createGraphDaily(cryptocurrency, currency)
        image = Image.open("assets/images/Line_Graph_Diagram.png")
        image = image.resize((360, 270))
        image = ImageTk.PhotoImage(image)
        self.graphDisplay.configure(image=image)
        self.graphDisplay.image = image
        self.graphDisplay.place(relx=0.5,rely=0.5, anchor="center")
        self.okayBtn.pack(side='right', padx=30, ipady=3)
 

    def showMonthlyGraph(self, cryptocurrency, currency):
        self.geometry("360x360")
        self.createGraphMonthly(cryptocurrency, currency)
        image = Image.open("assets/images/Line_Graph_Diagram.png")
        image = image.resize((360, 270))
        image = ImageTk.PhotoImage(image)
        self.graphDisplay.configure(image=image)
        self.graphDisplay.image = image
        self.graphDisplay.place(relx=0.5,rely=0.5, anchor="center")
        self.okayBtn.pack(side='right', padx=30, ipady=3)
        
    def close(self) -> None:
        self.destroy()
        
        
    def setup_window(self) -> None:
        
        self.overrideredirect(True)  # remove application from Window's window manager
        self.after_idle(self.lift)
        self.after(10, self.set_app_window)
        self.bind('<Map>', self.frame_mapped)
        self.z = 0  # used as a flag for mapping frames
        
        self.geometry('350x250')
        self.configure(borderwidth=1, relief='solid')
        
        body = ttk.Frame(self)
        body.pack(side='top', fill='both', expand=True)
        
        self.messageLabel = ttk.Label(body, text=self._message, style='Messagebox.TLabel', font='arial 16')
        self.messageLabel.pack(fill='both', expand=True)
        
        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x')
        
        self.buttons = ttk.Frame(self, height=35)
        self.buttons.pack_propagate(False)
        self.buttons.pack(side='bottom', fill='x')
        
        # position window to center of screen
        user32 = windll.user32
        screenW, screenH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        x = int(screenW / 2) - int(self.winfo_width() / 2)
        y = int(screenH / 2) - int(self.winfo_height() / 2)
        self.geometry(f'+{x}+{y}')

        
    def set_app_window(self) -> None:
        hwnd = windll.user32.GetParent(self.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
                               
        self.wm_withdraw()
        self.after(10, self.wm_deiconify)
        
        
    def frame_mapped(self, event=None) -> None:
        """Called when the window raises a map event"""

        self.overrideredirect(True)
        self.after_idle(self.lift)
        
        if (self.z == 0):
            self.set_app_window()
            self.z = 1
            
            
    def setup_titlebar(self) -> None:
        self.titlebar = ttk.Frame(self, height=35)
        self.titlebar.pack_propagate(False)
        self.titlebar.pack(side='top', fill='x')
        self.titlebar.bind('<Button-1>', self.drag_window)
        
        tbBody = ttk.Frame(self.titlebar)
        tbBody.pack(side='top', fill='both', expand=True)
        tbBody.bind('<Button-1>', self.drag_window)
        
        theme = str(self.master.tk.call("ttk::style", "theme", "use")).split("-")[-1]
        
        if theme == "light":
            activebg = "#EEEEEE"
            pressedbg = "#E0E0E0"
        else:
            activebg = "#2f2f2f"
            pressedbg = "#232323"
        
        ttk.Separator(self.titlebar, orient='horizontal').pack(side='bottom', fill='x')
        
        self.root.style.configure("Messagebox.TLabel", anchor="center")
        self.root.style.configure("MessageboxButton.TLabel", anchor="center")
        self.root.style.map("MessageboxButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])
        
        # close image
        closeImage = tk.PhotoImage(file=IMAGE_PATH+ f"close_{theme}.png")
        closeImage = closeImage.subsample(6,6)
        
        # close button
        closeButton = ttk.Button(tbBody, image=closeImage, style='MessageboxButton.TLabel', command=self.close)
        closeButton.pack(side='right', fill='y', ipadx=16)
        closeButton.image = closeImage
        
        # title label
        title = ttk.Label(tbBody, text=self._title, style='Messagebox.TLabel', font='arial 16')
        title.pack(side='left', fill='y', padx=15)
        title.bind('<Button-1>', self.drag_window)
        
        
    def drag_window(self, event) -> None:
        startX, startY = event.x_root, event.y_root
        winX, winY = self.winfo_x() - startX, self.winfo_y() - startY
        
        
        def move_window(event) -> None:
            x, y = event.x_root + winX, event.y_root + winY
            self.geometry(f'+{x}+{y}')
            
            
        event.widget.bind('<B1-Motion>', move_window)

    def createGraphDaily(self, cryptocurrency, currency):
        plt.clf()
        dataValue = []

        for x in range(30):
            extractData = cryptocompare.get_historical_price_day(cryptocurrency, currency=currency, limit=30)[x]["high"]
            dataValue.append(extractData)

        plt.plot(dataValue)
        plt.title('High Prices last 30 days')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.ylabel(f"{cryptocurrency} Value ({currency})")
        plt.savefig("assets/images/Line_Graph_Diagram.png")

    def createGraphMonthly(self, cryptocurrency, currency):
        plt.clf()
        dataValue = []
    
        month, year = datetime.datetime.now().month, datetime.datetime.now().year-1
        for x in range(12):
            extractData = cryptocompare.get_historical_price(cryptocurrency, currency=currency, timestamp=datetime.datetime(year, month, 1))[cryptocurrency][currency]
            dataValue.append(extractData)
            print(month, year)
            month = month + 1
            if month == 13:
                month, year = 1, year+1
            

        plt.style.use('dark_background')
        plt.plot(dataValue)
        plt.title('High Prices last 12 Months')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.ylabel(f"{cryptocurrency} Value ({currency})")
        plt.savefig("assets/images/Line_Graph_Diagram.png")
            
            
    