from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog as fd, ttk
from sklearn.cluster import DBSCAN
import customtkinter
import winsound
import random


class create_gui():
    def __init__(self):
        super().__init__()
        self.root = customtkinter.CTk()
        self.y = None
        self.x = None
        self.Y_VALUE = None
        self.X_VALUE = None
        self.y_var = None
        self.x_var = None
        self.eps = None
        self.min_sample = None
        self.openfile_tree = None
        self.df = None
        self.df1 = None
        self.numeric_columns = None
        self.extract_data_tree = None
        self.labels = None
        self.createTreeView()
        self.createopenFileButton()
        self.showValuesButton()
        self.createEntry()
        self.dbscanButton()
        self.showPlot()

        self.root.mainloop()

    def createopenFileButton(self):
        Button(text="OPEN FILE CSV", command=self.open_csv).grid(row=0, column=0)

    def createTreeView(self):
        self.openfile_tree = ttk.Treeview()
        self.openfile_tree.grid(row=7, column=2, padx=50, pady=20)
        self.extract_data_tree = ttk.Treeview()
        self.extract_data_tree.grid(row=8, column=2, padx=50)

    def showValuesButton(self):
        Button(text="SHOW VALUES CHOSEN", command=self.get_values, borderwidth=1, width=20).grid(row=8, column=0)

    def dbscanButton(self):
        Button(text="RUN DBSCAN", command=self.algorithm, borderwidth=1, width=20).grid(row=11, column=0, pady=10)

    def showPlot(self):
        Button(text="SHOW PLOT", command=self.plt_scatter, borderwidth=1, width=20).grid(row=12, column=0)

    def createEntry(self):
        Label(self.root, text="EPSILON: ", borderwidth=1, width=20).grid(row=9, column=0)
        Label(self.root, text="MIN_SAMPLE: ", borderwidth=1, width=20).grid(row=10, column=0)
        self.eps = Entry(width=24, borderwidth=1)
        self.eps.grid(row=9, column=1)
        self.min_sample = Entry(width=24, borderwidth=1)
        self.min_sample.grid(row=10, column=1)

    def open_csv(self):
        my_file = fd.askopenfilename(title="Open CSV File", filetypes=(("CSV Files", ".csv"), ("All Files", "*.*")))
        if self.x is not None and self.y is not None:
            self.x.destroy()
            self.y.destroy()
        self.df = pd.read_csv(my_file)
        self.df.shape

        self.openfile_tree.delete(*self.openfile_tree.get_children())
        self.openfile_tree['column'] = list(self.df.columns)
        self.openfile_tree['show'] = 'headings'

        for col in self.openfile_tree['column']:
            self.openfile_tree.heading(col, text=col)

        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            self.openfile_tree.insert("", "end", values=row)

        self.numeric_columns = self.df._get_numeric_data().columns.values.tolist()

        self.X_VALUE = self.numeric_columns
        self.Y_VALUE = self.numeric_columns

        self.x_var = StringVar(self.root)
        self.y_var = StringVar(self.root)
        Label(self.root, text="X_AXIS_VALUE: ", borderwidth=1, width=20).grid(row=1, column=0)
        Label(self.root, text="Y_AXIS_VALUE: ", borderwidth=1, width=20).grid(row=2, column=0)
        self.x = OptionMenu(self.root, self.x_var, *self.X_VALUE)
        self.x.grid(row=1, column=1)
        self.y = OptionMenu(self.root, self.y_var, *self.Y_VALUE)
        self.y.grid(row=2, column=1)

    def get_values(self):
        self.df1 = self.df.iloc[:,
                   [self.df.columns.get_loc(self.x_var.get()), self.df.columns.get_loc(self.y_var.get())]].values
        self.extract_data_tree.delete(*self.extract_data_tree.get_children())
        column_df2 = [self.x_var.get(), self.y_var.get()]
        df2 = pd.DataFrame(self.df1, columns=column_df2)
        self.extract_data_tree['column'] = list(df2.columns)
        self.extract_data_tree['show'] = 'headings'

        for col in self.extract_data_tree['column']:
            self.extract_data_tree.heading(col, text=col)

        df2_rows = df2.to_numpy().tolist()
        for row in df2_rows:
            self.extract_data_tree.insert("", "end", values=row)

    def algorithm(self):
        dbscan = DBSCAN(eps=float(self.eps.get()), min_samples=int(self.min_sample.get()))
        self.labels = dbscan.fit_predict(self.df1)
        np.unique(self.labels)

    def plt_scatter(self):
        number_of_colors = 20

        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        for i in self.labels:
            plt.scatter(self.df1[self.labels == i, 0], self.df1[self.labels == i, 1], s=20, c=color[i])

        plt.xlabel(self.x_var.get())
        plt.ylabel(self.y_var.get())
        plt.show()


do = create_gui()
