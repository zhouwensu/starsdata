import matplotlib.colors as mcolors
import pandas as pd

from waterfall_view import WaterfallView
import collections
from operator import attrgetter
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt

PlotData = collections.namedtuple('PlotData', ['name', 'unit', 'series'])


class FFTWaterfallController:
    def __init__(self, speed_name: str, selected_data, selected_index: list, plot_notebook, plot_counter):
        self._selected_data = selected_data
        self._selected_index = selected_index
        self._plot_notebook = plot_notebook
        self._plot_counter = plot_counter
        self._plot_view = WaterfallView(self._plot_notebook, self._plot_counter, self)
        self._freq = 1000
        self._N = int(np.power(2, np.ceil(np.log2(self._freq))))  # 下一个最近二次幂
        self._fft_array = np.zeros([self._selected_data.count // self._freq, self._N // 2], dtype=float)
        self._counter = 0
        item_name, item_unit, item_data = self._selected_data.read_csv_data(self._selected_index)
        speed_series = item_data.iloc[:, 0]
        speed_avg = speed_series.rolling(1000, min_periods=1000, step=1000).mean()

        signal_series = item_data.iloc[:, -1]

        signal_series.rolling(1000, min_periods=1000, step=1000).apply(lambda x: self.FFT(x.values))

        self._ax = self._plot_view.ax

        fig, ax = plt.subplots()
        im = ax.imshow(self._fft_array)
        ax.set_title('Pan on the colorbar to shift the color mapping\n'
                     'Zoom on the colorbar to scale the color mapping')

        fig.colorbar(im, ax=ax, label='Interactive colorbar')

        plt.show()

    def FFT(self, data):
        FFT_y1 = np.abs(fft(data, self._N)) / self._freq * 2  # N点FFT 变化,但处于信号长度
        FFT_y1 = FFT_y1[range(int(self._N / 2))]  # 取一半
        self._fft_array[self._counter] = FFT_y1
        self._counter = self._counter + 1

        return 0
