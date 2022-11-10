import tkinter as tk  # python 3
from tkinter import ttk
from tkinter import messagebox
from data_model import TestData
from root_view import RootView
from tkinter import filedialog
from timeline_controller import TimelineController
from waterfall_controller import FFTWaterfallController
from tkinter import messagebox as msg
from asammdf import MDF, Signal
import numpy as np
import pandas as pd


class RootController:
    def __init__(self):
        self.data_location = []
        self.test_data = []
        self.plot_view = []
        self.view = RootView(self)
        self.plot_counter = 0
        self.calc_counter = 0

    def run(self):
        self.view.mainloop()

    def new_dialog(self):
        pass

    def export_mdf4(self):
        selected_item = self.view.tree_frame.tree.selection()
        try:
            data_parent = self.view.tree_frame.tree.parent(selected_item[0])
            if data_parent == '':
                data_parent = selected_item[0]
            data_index = self.view.tree_frame.tree.index(data_parent)
            selected_data = self.test_data[data_index]
        except (ValueError, IndexError) as e:
            tk.messagebox.showinfo('Error', 'Open ' + str(e) + ' error')
        else:
            filename = filedialog.asksaveasfilename(title="Export to MDF4", initialdir=selected_data.data_path,
                                                    filetypes={("MDF4 File", "mf4")})
            with MDF(version='4.10') as mdf4:
                item_name, item_unit, item_timeline, item_data = selected_data.open_file_data_all()
                mdf4.start_time = pd.to_datetime(item_timeline[0])

                timeline_f = item_timeline.astype("float") / 1000000000
                timeline_f -= timeline_f[0]
                sigs = []
                for name, unit in zip(item_name, item_unit):
                    data = item_data[name].to_numpy()
                    if data.dtype == "object":
                        str_list = ['{}'.format(j).encode('ascii')
                                    for j in data]

                        sig = Signal(np.array(str_list),
                                     timeline_f,
                                     name=name,
                                     encoding='latin-1',
                                     )
                    else:
                        sig = Signal(data,
                                     timeline_f,
                                     name=name,
                                     unit=unit,
                                     conversion=None,
                                     )

                    sigs.append(sig)

                mdf4.append(sigs, comment=None, common_timebase=True)

                mdf4.save(dst=filename, overwrite=True)

    def plot_fft_waterfall_config(self):
        selected_item = self.view.tree_frame.tree.selection()
        data_parent = self.view.tree_frame.tree.parent(selected_item[0])
        if data_parent == '':
            msg.showerror("ERROR", "Wrong Data Selected")
        else:
            # ---------------- Show FFT Config------------------------------

            waterfall_config_view = tk.Toplevel()
            waterfall_config_view.title = "FFT Config"
            ttk.Label(waterfall_config_view, text="Speed Channel").grid(column=0, row=0)
            var = tk.StringVar()
            data_index = self.view.tree_frame.tree.index(data_parent)
            selected_data = self.test_data[data_index]
            name_tuple = tuple(selected_data.signal_names)
            speed_combobox = ttk.Combobox(waterfall_config_view, width=15, textvariable=var, value=name_tuple)
            speed_combobox.grid(column=0, row=1)
            plot_btn = ttk.Button(waterfall_config_view, text="OK",
                                  command=lambda: plot_fft_waterfall(speed_combobox.get()))
            plot_btn.grid(column=0, row=2)
            # ----------------------------------------------------------------

        def plot_fft_waterfall(speed_name):

            item_index = self.view.tree_frame.tree.index(selected_item[0])
            item_index_list = [item_index, ]
            speed_index = name_tuple.index(speed_name)
            item_index_list.append(speed_index)

            waterfall_config_view.destroy()
            plot_controller = FFTWaterfallController(speed_name, selected_data, item_index_list,
                                                     self.view.plot_notebook,
                                                     self.plot_counter)
            self.plot_view.append(plot_controller)
            self.view.update()
            self.plot_counter += 1

    def plot_timeline(self):
        selected_item = self.view.tree_frame.tree.selection()
        try:
            data_parent = self.view.tree_frame.tree.parent(selected_item[0])
            if data_parent == '':
                data_parent = selected_item[0]
            data_index = self.view.tree_frame.tree.index(data_parent)
            selected_data = self.test_data[data_index]
        except (ValueError, IndexError) as e:
            tk.messagebox.showinfo('Error', 'Open ' + str(e) + ' error')
        else:
            item_index_list = []
            for item in selected_item:
                if data_parent == self.view.tree_frame.tree.parent(item):  # Check if they belong to one Data
                    item_index = self.view.tree_frame.tree.index(item)
                    item_index_list.append(item_index)
            plot_controller = TimelineController(selected_data, item_index_list, self.view.plot_notebook,
                                                 self.plot_counter)
            self.plot_view.append(plot_controller)
            self.view.update()
            self.plot_counter += 1

    def close_data(self):
        selected_item = self.view.tree_frame.tree.selection()
        try:
            data_parent = self.view.tree_frame.tree.parent(selected_item[0])
            if data_parent == '':
                data_parent = selected_item[0]

            data_index = self.view.tree_frame.tree.index(data_parent)
        except (ValueError, IndexError) as e:
            tk.messagebox.showinfo('Error', 'Open ' + str(e) + ' error')
        else:
            self.data_location.remove(self.test_data[data_index].data_path)
            self.view.tree_frame.tree.delete(data_parent)
            del self.test_data[data_index]

    def save_dialog(self):
        pass

    # Open Data
    def open_dialog(self):
        file_path = filedialog.askopenfilenames(
            filetypes={("CSV Data", "*.csv"), ("MDF4 Data", "*.mf4"), ("MDF Data", "*.mdf"), ("INCA MDF", "*.dat")})
        if len(file_path) == 0:
            return
        else:
            self.open_test_file(file_path)

    def open_test_file(self, file_path):
        window_progressbar = tk.Tk()
        window_progressbar.title("Opening File...")
        window_progressbar.geometry("300x100")
        window_progressbar.resizable(width=False, height=False)
        mpb = tk.ttk.Progressbar(window_progressbar, orient="horizontal", length=300, mode="determinate")
        mpb.pack()
        mpb["maximum"] = len(file_path)
        mpb["value"] = 0

        for path_item in file_path:
            if path_item in self.data_location:
                tk.messagebox.showinfo('Error', str(path_item) + ' is already opened')
                continue

            else:
                try:
                    test_data = TestData(path_item)
                except Exception as e:
                    tk.messagebox.showinfo('Error', 'Open ' + str(e) + ' error')
                    mpb["value"] = mpb["value"] + 1
                    window_progressbar.update()
                else:
                    self.test_data.append(test_data)
                    self.data_location.append(path_item)
                    mpb["value"] = mpb["value"] + 1
                    window_progressbar.update()
        window_progressbar.destroy()
        self.show_data()

    def show_data(self):
        tree = self.view.tree_frame.tree
        exists_data_items = tree.get_children(item=None)
        exists_name = [tree.item(item, option='text') for item in exists_data_items]
        i = 0

        for data in self.test_data:
            if data.file_name in exists_name:
                continue
            else:
                tree_path_name = tree.insert('', 'end', text=data.file_name,
                                             value=i)
                i = i + 1
                j = 0
                for signal in data.signal:
                    tree.insert(tree_path_name, 'end', text=str(signal), value=j, )
                    j = j + 1
