import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class NotebookView(ttk.Frame):
    def __init__(self, container, controller, plot_counter):
        super().__init__(container)
        self.pack(side=tk.TOP, fill=tk.X)
        self._controller = controller
        self._container = container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._container.add(self, text="Plot " + str(plot_counter))

        self._figure = Figure(figsize=(5, 4), dpi=100)
        self._canvas = FigureCanvasTkAgg(self._figure, self)
        self._canvas.get_tk_widget().grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self._toolbar = NavigationToolbar2Tk(self._canvas, self, pack_toolbar=False)
        self._toolbar.update()
        self._toolbar.grid(column=0, row=1, sticky=tk.NSEW)

        ttk.Button(self, text="Config", command=self._controller.cfg_plot).grid(column=1, row=1)
        ttk.Button(self, text="Close", command=self._controller.del_plot).grid(column=2, row=1)

    def draw(self):
        self._canvas.draw()
