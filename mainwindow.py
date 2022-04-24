import tkinter as tk
from tkinter import ttk
import sv_ttk
from matplotlib import pyplot as plt
from PIL import ImageTk, Image

import server



class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons


        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        self.accentbutton = ttk.Button(
            self.widgets_frame, text="Make photo", style="Accent.TButton",command =(lambda: self.make_photo())
        )
        self.accentbutton.grid(row=7, column=0, padx=5, pady=20, sticky="nsew")


        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

    def make_photo(self):
        image = server.run()
        image = image.resize((1000, 800), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = ttk.Label(self.widgets_frame, image=img)
        panel.grid(row=20, column=0, padx=5, pady=80, sticky="nsew")
        panel.image = img


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