from steam.steamid import SteamID
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

import pyperclip
from functools import partial
import sqlite3
import ast

from os import walk
import importlib
import os.path as op

apps = []

# try:
#     style = ttk.Style(PageMain)
#     # style.theme_create("MyStyle", parent="alt", settings={
#     #         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
#     #         "TNotebook.Tab": {"configure": {"padding": [10, 10], "background": mygreen },
#     #         "map":       {"background": [("selected", "#dd0202")],
#     #                   "expand": [("selected", [1, 1, 1, 0])] } } } )
#     style.theme_create( "yummy", parent="alt", settings={
#     "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
#     "TNotebook.Tab": {
#         "configure": {"padding": [12, 10], "font" : ('URW Gothic L', '11', 'bold'), "background": "grey" },
#         "map":       {"background": [("selected", "#d2ffd2")],
#                       "expand": [("selected", [1, 1, 1, 0])] } } } )
#     style.theme_use("yummy")
# except:
#     pass

# style = ttk.Style()
# style.theme_create( "MyStyle", parent="alt", settings={
#         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
#         "TNotebook.Tab": {"configure": {"padding": [10, 10] },}})

# style.theme_use("MyStyle")
# style.map('TNotebook.Tab',background=[('selected', "#2F4DFF")])

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


def main_app(theme):
    global toggle_state
    Main = Tk()
    Main.title("Elitelupus Toolbox")
    # Main.geometry("720x296")
    Main.wm_attributes("-topmost", 1)
    # Main.wm_attributes("-toolwindow", True)
    # Main.overrideredirect(1)
    # Main.update()

    # Main.attributes('-alpha',0.8)
    Main.iconbitmap('icon.ico')


    try:
        style = ttk.Style(Main)


        style.theme_create( "LightTheme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
        "TFrame": {"configure": {"background": "white" } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 3], "font" : ('URW Gothic L', '10', 'bold'), "background": "grey" },
            "map":       {"background": [("selected", "#d2ffd2")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )


        style.theme_create( "DarkTheme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
        "TFrame": {"configure": {"background": "#121212" } },

        "TLabel": {"configure": {"background": "#121212",
                                "foreground": "#EDEDED"} },

        "TEntry": {"configure": {"background": "#121212",
                                "foreground": "#121212"} },

        "TButton": {"configure": {"background": "#121212",
                                "foreground": "#EDEDED",
                                "borderwidth": 2},

                    "map": {"background": [("selected", "#DA0037"),("active", "#DA0037")],
                                            "expand": [("active", [1, 1, 1, 0])]} },

        "TNotebook.Tab": {
            "configure": {"padding": [5, 3], "font" : ('URW Gothic L', '10', 'bold'), "background": "#444444", "foreground": "white"},
            "map":       {"background": [("selected", "#DA0037")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )


        # style.theme_use("LightTheme")
        # style.theme_use("DarkTheme")
        style.theme_use(str(theme))
        Main.configure(bg="#444444" if theme == "DarkTheme" else "white")
        if theme == "transparentGame":
            Main.wm_attributes("-transparentcolor", "#121212")
            Main.overrideredirect(1)
    except:
        pass



    toggle_state = 1
    def toggle_theme():
        global toggle_state
        print(toggle_state)
        if toggle_state == 1:
            Main.attributes('-alpha',0.8)
            Main.overrideredirect(1)

            toggle_state = 0
        else:
            Main.attributes('-alpha',1)
            Main.overrideredirect(0)

            toggle_state = 1



    menubar = Menu(Main)


    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Toggle Game Lock", command=toggle_theme)

    menubar.add_cascade(label="Settings", menu=filemenu)


    Main.config(menu=menubar)


    tab = {}
    # tabControl = ttk.Notebook(Main, width=Main.winfo_width())
    tabControl = ttk.Notebook(Main)

    for app, name in apps:
        tab.update({name: ttk.Frame(tabControl)})
        tabControl.add(tab[name], text=name.replace('_', ' '))

        app.main_app(frame=tab[name], theme=theme)

    tabControl.grid(row=0, column=0)

    Main.mainloop()

if __name__ == '__main__':
    # main_app(theme = "transparentGame")
    main_app(theme = "DarkTheme")
    # main_app(theme = "LightTheme")
