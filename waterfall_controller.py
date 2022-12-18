

from waterfall_view import WaterfallView
import collections
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.fftpack import fft
from notebook_controller import NotebookController

PlotData = collections.namedtuple('PlotData', ['name', 'unit', 'series'])


class FFTWaterfallController(NotebookController):

    def __init__(self, selected_data, selected_item, plot_notebook, plot_counter):
        super().__init__(selected_data, selected_item, plot_notebook, plot_counter)
        self._view = WaterfallView(self._plot_notebook, self, self._plot_counter)

        # ---------------- Show FFT Config------------------------------

        self._ax = None
        self._speed_index = None
        self._waterfall_config_view = tk.Toplevel()
        self._waterfall_config_view.title = "FFT Config"
        ttk.Label(self._waterfall_config_view, text="Speed Channel").grid(column=0, row=0)
        var = tk.StringVar()
        self._name_tuple = tuple(selected_data.signal_names)
        speed_combobox = ttk.Combobox(self._waterfall_config_view, width=15, textvariable=var, values=self._name_tuple)
        speed_combobox.grid(column=0, row=1)
        plot_btn = ttk.Button(self._waterfall_config_view, text="OK",
                              command=lambda: self.set_yaxis(speed_combobox.get()))
        plot_btn.grid(column=0, row=2)
        # ----------------------------------------------------------------

        self._freq = 1000
        self._N = int(np.power(2, np.ceil(np.log2(self._freq))))  # 下一个最近二次幂
        self._fft_array = np.zeros([self._selected_data.count // self._freq, self._N // 2], dtype=float)
        self._counter = 0
        item_name, item_unit, item_data = self._selected_data.read_csv_data(self._item_index_list)
        speed_series = item_data.iloc[:, 0]
        speed_avg = speed_series.rolling(1000, min_periods=1000, step=1000).mean()
        signal_series = item_data.iloc[:, -1]
        signal_series.rolling(1000, min_periods=1000, step=1000).apply(lambda x: self.fft(x.values))

    def fft(self, data):
        fft_y1 = np.abs(fft(data, self._N)) / self._freq * 2  # N点FFT 变化,但处于信号长度
        fft_y1 = fft_y1[range(int(self._N / 2))]  # 取一半
        self._fft_array[self._counter] = fft_y1
        self._counter = self._counter + 1

        return 0

    def cfg_plot(self):
        pass

    def del_plot(self):
        pass

    def set_yaxis(self, speed_name):
        self._speed_index = self._name_tuple.index(speed_name)
        self._waterfall_config_view.destroy()
        self.plot()

    def plot(self):
        self._view.plot_colormap(self._fft_array)
