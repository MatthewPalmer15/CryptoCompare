from tkinter import ttk
import tkinter as tk
import cryptocompare
import datetime

from assets import scripts

class Dashboard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.updating = False
        cryptocompare.cryptocompare._set_api_key_parameter("02a2c461980e076db08fea7971d9a41511dff6893b60fac034275c61cc591e48")
######################################################################################
#   User Entry
        self.cryptoLabel = ttk.Label(self, text="Cryptocurrency:", style="TLabel", font=('Courier', 9, "bold")).place(relx=0.25, rely=0.1, anchor='center')
        self.cryptoCurrency = ["BTC", "ETH", "DOGE", "BNB", "ADA", "XRP", "SOL", "DOT", "UNI", "LTC", "BCH","XLM", "LINK", "XMR", "BAT"]
        self.cryptoCurrency = sorted(self.cryptoCurrency)
        self.cryptoChoice = tk.StringVar()
        self.cryptoBox = ttk.OptionMenu(self, self.cryptoChoice, self.cryptoCurrency[0], *self.cryptoCurrency, style="TOptionMenu").place(relx=0.25, rely=0.2, anchor='center', width=250)

        self.currencyLabel = ttk.Label(self, text="Currency:", style="TLabel", font=('Courier', 9, "bold")).place(relx=0.25, rely=0.3, anchor='center')
        self.currentCurrency = ["USD", "GBP", "EUR", "JPY", "AUD", "CAD"]
        self.currentCurrency = sorted(self.currentCurrency)
        self.currency = tk.StringVar()
        self.currencyBox = ttk.OptionMenu(self, self.currency, self.currentCurrency[0], *self.currentCurrency, style="TOptionMenu").place(relx=0.25, rely=0.4, anchor='center', width=250)

        self.cryptoLabel = ttk.Label(self, text="Date:", style="TLabel", font=('Courier', 9, "bold")).place(relx=0.25, rely=0.5, anchor='center')
        self.day = tk.StringVar()
        self.day.set(datetime.datetime.now().day)
        self.dayBox = ttk.Spinbox(self, from_=1, to=31, textvariable=self.day, wrap=True, state = 'readonly', style="TSpinbox").place(relx=0.13, rely=0.6, anchor='center', width=90)

        self.month = tk.StringVar()
        self.month.set(datetime.datetime.now().month)
        self.monthBox = ttk.Spinbox(self, from_=1, to=12, textvariable=self.month, wrap=True, state = 'readonly', style="TSpinbox").place(relx=0.2475, rely=0.6, anchor='center', width=90)

        self.year = tk.StringVar()
        self.year.set(datetime.datetime.now().year)
        self.yearBox = ttk.Spinbox(self, from_=2012, to=datetime.datetime.now().year, textvariable=self.year, wrap=True, state = 'readonly', style="TSpinbox").place(relx=0.371, rely=0.6, anchor='center', width=100)

######################################################################################
#   Buttons
        self.calculateButton = ttk.Button(self, text="Calculate", command=self.onConvert, style="Accent.TButton")
        self.calculateButton.place(relx=0.75, rely=0.74, anchor='center', width=300)

        self.backButton = ttk.Button(self, text="Back", command=lambda: self.master.loadframe("Home"), style="TButton")
        self.backButton.place(relx=0.75, rely=0.85, anchor='center', width=300)

        self.dailyGraphActivateButton = ttk.Button(self, text="Show Daily Graph", command=lambda: scripts.Messagebox(self, title=f"{self.cryptoChoice.get()} Value (30 Days)", message="").showDailyGraph(cryptocurrency=self.cryptoChoice.get(), currency=self.currency.get()), style="TButton")
        self.dailyGraphActivateButton.place(relx=0.25, rely=0.74, anchor='center', width=300)

        self.dailyGraphActivateButton = ttk.Button(self, text="Show Monthly Graph", command=lambda: scripts.Messagebox(self, title=f"{self.cryptoChoice.get()} Value (12 Months)", message="").showMonthlyGraph(cryptocurrency=self.cryptoChoice.get(), currency=self.currency.get()), style="TButton")
        self.dailyGraphActivateButton.place(relx=0.25, rely=0.85, anchor='center', width=300)


######################################################################################
#   Labels

        self.CPLabel = ttk.Label(self, text="Current Price: ", font=('Courier', 9, "bold"), style="TLabel")
        self.CPLabel.place(relx=0.75, rely=0.1, anchor='center')
        self.currentPrice = ttk.Label(self, font=('Courier', 9, "bold"), style="TLabel")
        self.currentPrice.place(relx=0.75, rely=0.15, anchor='center')

        self.HPLabel = ttk.Label(self, text="High Price (24h): ", font=('Courier', 9, "bold"), style="TLabel")
        self.HPLabel.place(relx=0.75, rely=0.25, anchor='center')
        self.highPrice24 = ttk.Label(self, font=('Courier', 9, "bold"), style="TLabel")
        self.highPrice24.place(relx=0.75, rely=0.3, anchor='center')

        self.LPLabel = ttk.Label(self, text="Low Price (24h): ", font=('Courier', 9, "bold"), style="TLabel")
        self.LPLabel.place(relx=0.75, rely=0.4, anchor='center')
        self.lowPrice24 = ttk.Label(self, font=('Courier', 9, "bold"), style="TLabel")
        self.lowPrice24.place(relx=0.75, rely=0.45, anchor='center')

        self.HPLabel2 = ttk.Label(self, text="Price at Date ", font=('Courier', 9, "bold"), style="TLabel")
        self.HPLabel2.place(relx=0.75, rely=0.55, anchor='center')
        self.historyPrice = ttk.Label(self, font=('Courier', 9, "bold"), style="TLabel")
        self.historyPrice.place(relx=0.75, rely=0.6, anchor='center')

######################################################################################
#   Functions

    def updateInfo(self):
        infoGatherCP = cryptocompare.get_price(self.cryptoChoice.get(), currency=str(self.currency.get()))
        infoGather = cryptocompare.get_avg(self.cryptoChoice.get(), currency=str(self.currency.get()))
        highest24hour = infoGather["HIGH24HOUR"]
        lowest24hour = infoGather["LOW24HOUR"]
        historyPriceDate = cryptocompare.get_historical_price(self.cryptoChoice.get(), currency=str(self.currency.get()), timestamp=datetime.datetime(int(self.year.get()),int(self.month.get()),int(self.day.get())))

        self.currentPrice.configure(text=str(round(infoGatherCP[self.cryptoChoice.get()][self.currency.get()] , 5)) + " " + self.currency.get())
        self.highPrice24.configure(text=str(round(highest24hour, 5)) + " " + self.currency.get())
        self.lowPrice24.configure(text=str(round(lowest24hour, 5)) + " " + self.currency.get())
        self.historyPrice.configure(text=str(round(historyPriceDate[self.cryptoChoice.get()][self.currency.get()] , 5)) + " " + self.currency.get())

        if self.updating:
                self.after(1000, self.updateInfo)
        
    def onConvert(self):
        self.updating = not self.updating
        if self.updating:
            self.updateInfo()
######################################################################################