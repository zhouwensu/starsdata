
import abc


class NotebookController(abc.ABC):
    def __init__(self, selected_data, item_index_list, plot_notebook, plot_counter):
        self._selected_data = selected_data
        self._item_index_list = item_index_list
        self._plot_notebook = plot_notebook
        self._plot_counter = plot_counter

    @abc.abstractmethod
    def plot(self):
        pass
        """show plot"""

    @abc.abstractmethod
    def del_plot(self):
        pass

    @abc.abstractmethod
    def cfg_plot(self):
        pass



