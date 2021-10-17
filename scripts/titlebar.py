import tkinter as tk
from tkinter import ttk
from ctypes import windll


IMAGE_PATH = "assets/images/"  # replace with your image path (remember to add a / on the end)

# Windows OS styles for custom taskbar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


class Titlebar(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        
        self.prepare_root_window()

        self.pack_propagate(False)
        self.configure(height=35)
        self.bind("<Button-1>", self.drag_window)
        
        self.closeButton = ttk.Button(self, style="TitlebarButton.TLabel", takefocus=False, command=self.close_window)
        self.closeButton.pack(side="right", fill="y", ipadx=6)
        
        self.minimizeButton = ttk.Button(self, style="TitlebarButton.TLabel", takefocus=False, command=self.minimize_window)
        self.minimizeButton.pack(side="right", fill="y", ipadx=6)

        self.settingsButton = ttk.Button(self, style="TitlebarButton.TLabel", takefocus=False, command=lambda: self.master.loadframe("Settings"))
        self.settingsButton.pack(side="right", fill="y", ipadx=6)
        
        titleLabel = ttk.Label(self, text=self.master.title(), font=("HP Simplified Hans Light", 12))
        titleLabel.pack(side="left", fill="y")
        titleLabel.bind("<Button-1>", self.drag_window)
        
        self.logoLabel = ttk.Label(self, style="Titlebar.TLabel")
        self.logoLabel.pack(side="left", padx=5, before=titleLabel)
        self.logoLabel.bind("<Button-1>", self.drag_window)
        
        self.configure_style()
        
        
    def drag_window(self, event) -> None:
        startX, startY = event.x_root, event.y_root
        winX, winY = self.master.winfo_x() - startX, self.master.winfo_y() - startY
        
        def move_window(event) -> None:
            x, y = event.x_root + winX, event.y_root + winY
            self.master.geometry(f'+{x}+{y}')
            
        event.widget.bind('<B1-Motion>', move_window)
        
        
    def minimize_window(self) -> None:  
        self.master.state('withdrawn')
        self.master.overrideredirect(False)
        self.master.state('iconic')
        self.master.z = 0
        
        
    def close_window(self) -> None:
        self.master.closeApplication()
        
        
    def configure_style(self) -> None:
        theme = str(self.master.tk.call("ttk::style", "theme", "use")).split("-")[-1]
        
        if theme == "light":
            activebg = "#EEEEEE"
            pressedbg = "#E0E0E0"
        else:
            activebg = "#2f2f2f"
            pressedbg = "#232323"
        
        self.master.style.configure("Titlebar.TLabel", anchor="center")
        self.master.style.configure("TitlebarButton.TLabel", anchor="center")
        self.master.style.map("TitlebarButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])
        
        closeImg = tk.PhotoImage(file=IMAGE_PATH + f"close_{theme}.png")
        closeImg = closeImg.subsample(6,6)
        
        minImg = tk.PhotoImage(file=IMAGE_PATH + f"minimize_{theme}.png")
        minImg = minImg.subsample(6,6)

        settingsImg = tk.PhotoImage(file=IMAGE_PATH + f"settings_{theme}.png")
        settingsImg = settingsImg.subsample(6,6)
        
        iconImg = tk.PhotoImage(file=IMAGE_PATH + f"logo_{theme}.png")
        iconImg = iconImg.subsample(6,6)
        
        self.closeButton.configure(image=closeImg)
        self.closeButton.image = closeImg
        
        self.minimizeButton.configure(image=minImg)
        self.minimizeButton.image = minImg

        self.settingsButton.configure(image=settingsImg)
        self.settingsButton.image = settingsImg
        
        self.logoLabel.configure(image=iconImg)
        self.logoLabel.image = iconImg
        
        
    def prepare_root_window(self) -> None:
        self.master.overrideredirect(True)
        self.master.after(10, self.set_app_window)
        self.master.bind("<Map>", self.frame_mapped)
        self.master.z = 0
        
        
    def set_app_window(self) -> None:
        hwnd = windll.user32.GetParent(self.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
                               
        self.master.wm_withdraw()
        self.master.after(10, self.master.wm_deiconify)
        
        
    def frame_mapped(self, event) -> None:
        self.master.overrideredirect(True)
        
        if (self.master.z == 0):
            self.set_app_window()
            self.master.z = 1



#           USAGE EXAMPLE v

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    root.style = ttk.Style(root)
    root.titlebar = Titlebar(root)
    root.titlebar.pack(side="top", fill="x")
    root.mainloop()
