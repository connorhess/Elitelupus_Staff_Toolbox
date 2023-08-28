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
from cefpython3 import cefpython as cef
import platform
import sys
import webbrowser
import threading
import time


import tkinter as tk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        container.update()
        canvas = tk.Canvas(self, height=container.winfo_height())
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, background="black", height=container.winfo_height())

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def main_app(frame=None, theme="DarkTheme"):
    if frame == None:
        Page1 = Tk()
        Page1.title("Elitelupus Refund Template Maker")
    else:
        Page1 = frame

    frame_width = 445
    frame_height1 = 100
    frame_height2 = 120

    def Web_browser_forums():
        new = 2
        webbrowser.open("https://elitelupus.com/forums/",new=new)

    def WB_open(Url):
        new = 2
        webbrowser.open(Url,new=new)

    def Web_Page(Url):
    # def WB_open(Url):
        # Page.iconify()
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize()
        cef.CreateBrowserSync(url=Url, window_title="ToolBox")
        cef.MessageLoop()
        cef.Shutdown()


    F2 = ttk.Frame(Page1, height=frame_height2, width=frame_width)
    F2.grid(row=1,column=0)
    F2.grid_propagate(0)

    myFont2 = Font(family="Times New Roman", size=14)
    width2 = 24
    BG = "light green"
    FG = "black"

    B3 = ttk.Button(F2, text="Ban Appeal", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=15"))
    B3.grid(row=0,column=0)

    B4 = ttk.Button(F2, text="Warn Appeal", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=25"))
    B4.grid(row=0,column=1)

    B5 = ttk.Button(F2, text="Staff Applications", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=14"))
    B5.grid(row=0,column=2)


    B6 = ttk.Button(F2, text="Player Reports", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=16"))
    B6.grid(row=1,column=0)

    B7 = ttk.Button(F2, text="Rules", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/showthread.php?tid=6355"))
    B7.grid(row=1,column=1)

    B8 = ttk.Button(F2, text="Job Rules", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/showthread.php?tid=8627"))
    B8.grid(row=1,column=2)


    B9 = ttk.Button(F2, text="Staff Reports", width=width2, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=17"))
    B9.grid(row=2,column=0)



    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
