from steam.steamid import SteamID
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pyperclip
from functools import partial
import sqlite3
import ast

from os import walk
import importlib
import os.path as op

apps = []


blueprint_dirnames = []
for (dirpath, dirnames, filenames) in walk(op.dirname(__file__)):
    blueprint_dirnames.extend(dirnames)
    break

for lib in blueprint_dirnames:
    try:
        if str(lib) != ".git":
            print(lib)
            lib_mod = f'{lib}.main'
            # cls = getattr(importlib.import_module(lib_mod), "main_app")
            cls = (importlib.import_module(lib_mod))
            apps.append((cls, str(lib)))
            print(f"Successfully imported blueprint: {lib}")
    except Exception as e:
        print("error", e)


def main_app():
    Main = Tk()
    Main.title("Elitelupus Toolbox")
    # Main.geometry("720x296")
    Main.wm_attributes("-topmost", 1)
    # Main.update()

    tab = {}
    # tabControl = ttk.Notebook(Main, width=Main.winfo_width())
    tabControl = ttk.Notebook(Main)

    for app, name in apps:
        tab.update({name: ttk.Frame(tabControl)})
        tabControl.add(tab[name], text=name.replace('_', ' '))

        app.main_app(frame=tab[name])

    tabControl.grid(row=0, column=0)

    Main.mainloop()

if __name__ == '__main__':
    main_app()
