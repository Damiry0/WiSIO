"""
Example script for testing the Sun Valley theme
Author: rdbende
License: GNU GPLv3 license
Source: https://github.com/rdbende/ttk-widget-factory
"""


import tkinter as tk
from tkinter import ttk
import sv_ttk



class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons
        self.check_frame = ttk.LabelFrame(self, text="Checkbuttons", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(80, 10), pady=(20, 10), sticky="nsew"
        )

        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple example")

    # Simply set the theme
    sv_ttk.set_theme("dark")  # Set dark theme
    sv_ttk.use_dark_theme()  # Set dark theme

    # root.tk.call("source", "sun-valley.tcl")
    # root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    # root.minsize(root.winfo_width(), root.winfo_height())
    # x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    # y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    # root.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    root.geometry("600x400")

    root.mainloop()