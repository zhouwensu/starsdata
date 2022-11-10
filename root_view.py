import tkinter as tk
from tkinter import ttk


class RootView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        # Add a title
        self.title("STARS Data")

        self.geometry('640x480')
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.controller = controller

        # Add Tree Viewer
        self.tree_frame = self.TreeFrame(self)
        self.tree_frame.grid(column=0, row=0, sticky=tk.NSEW)
        # Add Plot Viewer
        self.plot_notebook = ttk.Notebook(self)
        self.plot_notebook.grid(column=1, row=0, sticky=tk.NSEW)

        # Creating a Menu Bar
        self.menu_bar = self.init_main_menu_bar()
        self.config(menu=self.menu_bar)

    def init_main_menu_bar(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.controller.new_dialog)
        file_menu.add_command(label='Open', command=lambda: self.controller.open_dialog())
        file_menu.add_command(label='Save', command=self.controller.save_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)

        plot_menu = self.init_plot_menu(menu_bar)
        menu_bar.add_cascade(label='Plot', menu=plot_menu)
        analysis_menu = self.init_analysis_menu(menu_bar)
        menu_bar.add_cascade(label='Analysis', menu=analysis_menu)
        return menu_bar

    def init_tree_menu_bar(self, parent):
        tree_menu = tk.Menu(parent, tearoff=0)
        plot_menu = self.init_plot_menu(tree_menu)
        tree_menu.add_cascade(label='Plot', menu=plot_menu)
        export_menu = self.init_export_menu(tree_menu)
        tree_menu.add_cascade(label='Export', menu=export_menu)
        analysis_menu = self.init_analysis_menu(tree_menu)
        tree_menu.add_cascade(label='Analysis', menu=analysis_menu)
        tree_menu.add_command(label='Close', command=self.controller.close_data)
        return tree_menu

    def init_plot_menu(self, parent):
        plot_menu = tk.Menu(parent, tearoff=0)
        plot_menu.add_command(label='Plot Timeline', command=self.controller.plot_timeline)
        plot_menu.add_command(label='Plot FFT Waterfall', command=self.controller.plot_fft_waterfall_config)
        return plot_menu

    def init_export_menu(self, parent):
        export_menu = tk.Menu(parent, tearoff=0)
        export_menu.add_command(label='MDF4', command=self.controller.export_mdf4)
        return export_menu

    def init_analysis_menu(self, parent):
        analysis_menu = tk.Menu(parent, tearoff=0)
        calc_menu = tk.Menu(analysis_menu, tearoff=0)
        analysis_menu.add_cascade(label='Calculate', menu=calc_menu)
        return analysis_menu

    class TreeFrame(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.tree = ttk.Treeview(self, show='tree')
            sb = tk.Scrollbar(self)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.config(yscrollcommand=sb.set)
            sb.config(command=self.tree.yview)
            self.tree.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)
            self.menu = parent.init_tree_menu_bar(self.tree)
            self.tree.bind("<Button-3>", self.tf_pop_up)

        def tf_pop_up(self, event):
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()
