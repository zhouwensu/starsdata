import tkinter as tk
from notebook_view import NotebookView
from matplotlib.axes import Axes
from matplotlib.ticker import AutoMinorLocator


class TimelineView(NotebookView):
    def __init__(self, container, controller, plot_counter):
        super().__init__(container, controller, plot_counter)

        self._ax = self._figure.add_subplot(111)  # type:Axes
        self._ax.grid(True, linestyle='-.')
        self._ax.xaxis.set_minor_locator(AutoMinorLocator())

    def plot_timeline(self, time_line, data, name):
        self._ax.plot(time_line, data, label=name)

    def legend(self):
        self._ax.legend()

    class PlotSetting(tk.Toplevel):
        def __init__(self, item_name, item_unit):
            super().__init__()
            self.title("Plot Config")

    @property
    def ax(self):
        return self._ax
