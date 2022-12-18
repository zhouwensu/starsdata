import matplotlib.colors as mcolors
from timeline_view import TimelineView
import collections
from operator import attrgetter
from notebook_controller import NotebookController

PlotData = collections.namedtuple('PlotData', ['name', 'unit', 'series'])


class TimelineController(NotebookController):

    def __init__(self, selected_data, item_index_list, plot_notebook, plot_counter):
        super().__init__(selected_data, item_index_list, plot_notebook, plot_counter)
        self._view = TimelineView(self._plot_notebook, self, self._plot_counter)
        self._ax = self._view.ax

        item_name, item_unit, item_data = self._selected_data.read_csv_data(self._item_index_list)
        self._time_line = self._selected_data.timeline
        self._plot_data = [PlotData(name, unit, series)
                           for unit, [name, series] in zip(item_unit, item_data.items())]
        self._plot_data.sort(key=attrgetter('unit'))
        self._plot = []
        self.plot()

    def plot(self):
        ax_counter = 0
        unit_memo = None
        colors = list(mcolors.XKCD_COLORS)
        colors_index = 0
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
                    self._ax = self._view.ax.twinx()
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
        self._view.ax.legend(handles=self._plot)
        self._view.draw()

    def del_plot(self):
        self._view.destroy()

    def cfg_plot(self):
        pass
