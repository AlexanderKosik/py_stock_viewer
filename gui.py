from tkinter import *
from tkinter.ttk import *

import numpy as np
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rcParams

import stock_data

sns.set(style="darkgrid")
rcParams['figure.subplot.bottom'] = 0.2

class MainGUI:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Python Stock Viewer")

        self.lbl_stock = Label(master=self.root, text="Ticker: ").grid(column=0, row=0, sticky=W)
        self.txt_stock = Combobox(master=self.root)
        self.txt_stock['values'] = ("ARL.F", "GOOGL", "DBK.DE", "TSLA", "AMZN")
        self.txt_stock.current(0)
        self.txt_stock.grid(column=1, row=0, sticky=W+E)
        self.txt_stock.bind("<Return>", self._update_stock_chart)

        self.lbl_avg_short = Label(master=self.root, text="Short AVG: ").grid(column=0, row=1)
        self.txt_avg_short = Spinbox(master=self.root, from_=0.0, to=50, increment=1)
        self.txt_avg_short.set(10)
        self.txt_avg_short.grid(column=1, row=1)

        self.lbl_avg_long = Label(master=self.root, text="Long AVG: ").grid(column=0, row=2)
        self.txt_avg_long = Spinbox(master=self.root, from_=10.0, to=1000, increment=5)
        self.txt_avg_long.set(50)
        self.txt_avg_long.grid(column=1, row=2)

        # Add a update button
        self.btn_update = Button(master=self.root, text="Update", command=self._update_stock_chart).grid(column=1, row=3, sticky=W+E)

        self._update_stock_chart()

    def _create_stock_chart(self):
        figure = Figure(figsize=(13, 5), dpi=100)
        a = figure.add_subplot()
        stock_config = stock_data.StockConfig(self.txt_stock.get(), int(self.txt_avg_short.get()), int(self.txt_avg_long.get()))
        data = stock_data.StockData(stock_config)
        ax = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.closing, label="Closing price", ax=a)
        ay = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.avg_short, label="Rolling avg short", ax=a)
        az = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.avg_long, label="Rolling avg long", ax=a)
        return figure

    def _update_stock_chart(self, *_): # *_ to be used with events
        self.figure = self._create_stock_chart()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=2, row=0, rowspan=25)


sns.set()
gui = MainGUI()

mainloop()