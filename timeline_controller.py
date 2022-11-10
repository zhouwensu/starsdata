import matplotlib.colors as mcolors
from timeline_view import ChartView
import collections
from operator import attrgetter

PlotData = collections.namedtuple('PlotData', ['name', 'unit', 'series'])


class TimelineController:
    def __init__(self, selected_data, selected_item, plot_notebook, plot_counter):
        self._selected_data = selected_data
        self._selected_item = selected_item
        self._plot_notebook = plot_notebook
        self._plot_counter = plot_counter
        self._plot_view = ChartView(self._plot_notebook, self._plot_counter, self)
        item_name, item_unit, item_data = self._selected_data.read_csv_data(self._selected_item)
        self._time_line = self._selected_data.timeline
        self._plot_data = [PlotData(name, unit, series)
                           for unit, [name, series] in zip(item_unit, item_data.iteritems())]
        self._plot_data.sort(key=attrgetter('unit'))
        ax_counter = 0
        unit_memo = None
        self._ax = self._plot_view.ax
        colors = list(mcolors.XKCD_COLORS)
        colors_index = 0
        self._plot = []
        for data in self._plot_data:
            if unit_memo != data.unit:
                if ax_counter == 0:
                    p, = self._ax.plot(self._time_line, data.series, color=mcolors.XKCD_COLORS[colors[colors_index]],
                                       label=data.name)
                    self._ax.set_ylabel(data.unit)
                    self._plot.append(p)
                    unit_memo = data.unit
                    colors_index = colors_index + 1
                    ax_counter = ax_counter + 1
                else:
                    self._ax = self._plot_view.ax.twinx()
                    if ax_counter > 1:
                        position = 1 + (ax_counter - 1) * 0.1
                        self._ax.spines.right.set_position(("axes", position))
                    p, = self._ax.plot(self._time_line, data.series, color=mcolors.XKCD_COLORS[colors[colors_index]],
                                       label=data.name)

                    self._ax.set_ylabel(data.unit)

                    self._plot.append(p)
                    ax_counter = ax_counter + 1
                    colors_index = colors_index + 1

                    unit_memo = data.unit
            else:
                p, = self._ax.plot(self._time_line, data.series, color=mcolors.XKCD_COLORS[colors[colors_index]],
                                   label=data.name)
                self._plot.append(p)
                unit_memo = data.unit
                colors_index = colors_index + 1
        self._plot_view.ax.legend(handles=self._plot)

    def del_plot(self):
        self._plot_view.destroy()

    def cfg_plot(self):
        pass
