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
        self.show_divs = IntVar()
        self.cb_show_divs = Checkbutton(master=self.root, text="Show Dividends", var=self.show_divs, onvalue = 1, offvalue = 0)
        self.cb_show_divs.grid(column=1, row=3, sticky=W)

        # Add a update button
        self.btn_update = Button(master=self.root, text="Update", command=self._update_stock_chart).grid(column=1, row=4, sticky=W+E)

        self._update_stock_chart()

    def _create_stock_chart(self):
        # query data
        stock_config = stock_data.StockConfig(self.txt_stock.get(), int(self.txt_avg_short.get()), int(self.txt_avg_long.get()))
        data = stock_data.StockData(stock_config)

        # check if dividend data is available
        dividend_greater_zero = data.data['Dividends'] > 0.0
        divs = data.data[dividend_greater_zero]

        figure = Figure(figsize=(16, 8), dpi=100)
        # check if we have divs and should draw divs
        if self.show_divs.get() == 1 and divs.empty is False:
            stock_plot = figure.add_subplot(121)
            dividend_plot = figure.add_subplot(122)
            divs['Dividends'].index = divs['Dividends'].index.strftime("%Y")
            if all(divs['Dividends'].values):
                sns.barplot(x=divs['Dividends'].index, y=divs['Dividends'].values, palette="rocket", ax=dividend_plot)
        else:
            # draw only single chart
            stock_plot = figure.add_subplot(111)

        ax = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.closing, label="Closing price", ax=stock_plot)
        ay = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.avg_short, label="Rolling avg short", ax=stock_plot)
        az = sns.lineplot(hue="Events", dashes=False, markers=True, data=data.avg_long, label="Rolling avg long", ax=stock_plot)

        return figure

    def _update_stock_chart(self, *_): # *_ to be used with events
        self.figure = self._create_stock_chart()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=2, row=0, rowspan=25)


sns.set()
gui = MainGUI()

mainloop()