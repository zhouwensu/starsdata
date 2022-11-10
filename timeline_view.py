import tkinter as tk
from tkinter import ttk
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import AutoMinorLocator


class ChartView(ttk.Frame):
    def __init__(self, container, plot_counter, controller):
        super().__init__(container)
        self.pack(side=tk.TOP, fill=tk.X)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        container.add(self, text="Plot " + str(plot_counter))

        figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = figure.add_subplot(111)  # type:Axes
        self.ax.grid(True, linestyle='-.')
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())

        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(column=0, row=1, sticky=tk.NSEW)

        ttk.Button(self, text="Config", command=self.controller.cfg_plot).grid(column=1, row=1)
        ttk.Button(self, text="Close", command=self.controller.del_plot).grid(column=2, row=1)

    def plot_timeline(self, time_line, data, name):
        self.ax.plot(time_line, data, label=name)

    def legend(self):
        self.ax.legend()

    class PlotSetting(tk.Toplevel):
        def __init__(self, item_name, item_unit):
            super().__init__()
            self.title("Plot Config")
