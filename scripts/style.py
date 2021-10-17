from tkinter import ttk

class Style(ttk.Style):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.configure("Accent.TButton", font=('Courier', 9, "bold"))
        self.configure("TEntry", font=('Courier', 9, "bold"))
        self.configure("TOptionMenu", font=('Courier', 9, "bold"))
        self.configure("TButton", font=('Courier', 9, "bold"))
        self.configure("Switch.TCheckbutton", font=('Courier', 9, "bold"))