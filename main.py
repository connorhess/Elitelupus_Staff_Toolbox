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
import sys

import os
import importlib
import os.path as op
from pypresence import Presence  # The simple rich presence client in pypresence
import time

for i in range(0, 10):
    try:
        RPC = Presence(893205771108622356, pipe=i)
        RPC.connect()
        # RPC.update(state="Rich Presence using pypresence!")  # Updates our presence
        startTime = int(time.time())
        RPC.update(details="Elitelupus Staff Toolbox",
                   start=startTime,
                   state="Staff Toolbox, Made By Connor2",
                   large_image="icon_512x512",
                   large_text="Staff Toolbox, Made By Connor2",
                   buttons=[{"label": "Elitelupus GMod Discord",
                             "url": "https://discord.gg/YKC74XH"},
                            {"label": "Elitelupus Meta Discord",
                             "url": "https://discord.gg/3H6x5kSt"}]
                   )
        print("Connected on pipe", i)
        break
    except:
        print(f"Discord Rich PresenceNot Working on pipe: {i}")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    Main.iconbitmap(resource_path('icon.ico'))

    def on_closing():
        Main.destroy()
        try:
            RPC.close()
        except:
            pass
        sys.exit()

    Main.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        style = ttk.Style(Main)

        style.theme_create("LightTheme", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0]}},
            "TFrame": {"configure": {"background": "white"}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 3], "font": ('URW Gothic L', '10', 'bold'), "background": "grey"},
                "map":       {"background": [("selected", "#d2ffd2")],
                              "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_create("DarkTheme", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0]}},
            "TFrame": {"configure": {"background": "#121212"}},

            "TLabel": {"configure": {"background": "#121212",
                                     "foreground": "#EDEDED"}},

            "Treeview": {"configure": {"fieldbackground": "#121212"} },
            "Treeview.Item": {"configure": {"foreground": "#121212"} },
            "Treeview.Heading": {"configure": {"background": "#121212",
                                                "foreground": "#EDEDED"} },

            "TEntry": {"configure": {"background": "#121212",
                                     "foreground": "#121212"}},

            "TButton": {"configure": {"background": "#121212",
                                      "foreground": "#EDEDED",
                                      "borderwidth": 2},

                        "map": {"background": [("selected", "#DA0037"), ("active", "#DA0037")],
                                "expand": [("active", [1, 1, 1, 0])]}},

            "TNotebook.Tab": {
                "configure": {"padding": [5, 3], "font": ('URW Gothic L', '10', 'bold'), "background": "#444444", "foreground": "white"},
                "map":       {"background": [("selected", "#DA0037")],
                              "expand": [("selected", [1, 1, 1, 0])]}}})

        # style.theme_use("LightTheme")
        # style.theme_use("DarkTheme")
        style.theme_use(str(theme))
        Main.configure(bg="#121212" if theme == "DarkTheme" else "white")
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
            Main.attributes('-alpha', 0.8)
            Main.overrideredirect(1)

            toggle_state = 0
        else:
            Main.attributes('-alpha', 1)
            Main.overrideredirect(0)

            toggle_state = 1

    menubar = Menu(Main)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Toggle Game Lock", command=toggle_theme)

    menubar.add_cascade(label="Settings", menu=filemenu)

    Main.config(menu=menubar)

    # tabControl = ttk.Notebook(Main, width=Main.winfo_width())
    tabControl = ttk.Notebook(Main)

    # Elitelupus_ban_search_frame = ttk.Frame(tabControl)
    # tabControl.add(Elitelupus_ban_search_frame, text=(
    #     "Elitelupus_ban_search").replace('_', ' '))
    # import Elitelupus_ban_search
    # Elitelupus_ban_search.main_app(frame=Elitelupus_ban_search_frame, theme=theme)


    Sit_Counter_frame = ttk.Frame(tabControl)
    tabControl.add(Sit_Counter_frame, text=("Sit_Counter").replace('_', ' '))
    import Sit_Counter
    Sit_Counter.main_app(frame=Sit_Counter_frame, theme=theme)


    Template_Maker_frame = ttk.Frame(tabControl)
    tabControl.add(Template_Maker_frame, text=(
        "Template_Maker").replace('_', ' '))
    import Template_Maker
    Template_Maker.main_app(frame=Template_Maker_frame, theme=theme)


    # Useful_Links_frame = ttk.Frame(tabControl)
    # tabControl.add(Useful_Links_frame, text=("Useful_Links").replace('_', ' '))
    # import Useful_Links
    # Useful_Links.main_app(frame=Useful_Links_frame, theme=theme)


    Stats_frame = ttk.Frame(tabControl)
    tabControl.add(Stats_frame, text="Stats")
    tabControl2 = ttk.Notebook(Stats_frame)

    try:
        Server_Status_frame = ttk.Frame(tabControl)
        tabControl2.add(Server_Status_frame, text=("Server_Status").replace('_', ' '))
        import Server_Status
        Server_Status.main_app(frame=Server_Status_frame, theme=theme)
    except Exception as e:
        print("issue with server_data; ", e)

    try:
        Staff_Distribution_frame = ttk.Frame(tabControl)
        tabControl2.add(Staff_Distribution_frame, text=("Staff_Distribution").replace('_', ' '))
        import Staff_Distribution
        Staff_Distribution.main_app(frame=Staff_Distribution_frame, theme=theme)
    except Exception as e:
        print("issue with Staff_Distribution; ", e)


    def routine(event):
        tab_name = (tabControl.tab(tabControl.select(), "text"))
        # startTime = int(time.time())
        try:
            RPC.update(details="Elitelupus Staff Toolbox",
                       start=startTime,
                       state=f"Viewing: {tab_name}",
                       large_image="icon_512x512",
                       large_text="Staff Toolbox, Made By Connor2",
                       buttons=[{"label": "Elitelupus Discord Server",
                                 "url": "https://discord.gg/YKC74XH"},
                                {"label": "Server Rules",
                                 "url": "https://elitelupus.com/forums/forumdisplay.php?fid=7"}]
                       )
        except:
            pass

    tabControl.bind("<<NotebookTabChanged>>", routine)

    tabControl.grid(row=0, column=0)
    tabControl2.grid(row=0, column=0)

    Main.mainloop()


if __name__ == '__main__':
    # main_app(theme = "transparentGame")
    main_app(theme="DarkTheme")
    # main_app(theme = "LightTheme")
