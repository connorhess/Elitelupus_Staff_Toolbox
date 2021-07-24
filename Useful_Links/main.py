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
        self.scrollable_frame = Frame(canvas, background="black", height=container.winfo_height())

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


def punishment_app():
    Page1 = Toplevel()
    Page1.title("Elitelupus Punishment Guidelines")
    # Page1.geometry("526x296")
    Page1.geometry("720x400")


    offences = {"Base": [{"name": 'Fail Base',           '1': 'Verbal Warn', '2': 'Warn', '3': 'Base Removal',   '4': 'Kick'},
                        {"name": 'Fading Door Abuse',   '1': 'Warn',        '2': 'Warn', '3': 'Warn + Kick',    '4': '12 Hour Ban'},
                        {"name": 'One-Way Shooting',    '1': 'Warn',        '2': 'Warn', '3': '12 Hour Ban',    '4': '3 Day Ban'}],

                "Jobs": [{"name": 'Mining as Non-Citizen/Miner', '1': 'Verbal Warn (Warn+Kick if AFK)', '2': 'Warn (Kick if AFK)', '3': '12 Hour Ban', '4': '36 Hour Ban'},
                        {"name": 'Minor Job Abuse',              '1': 'Warn',                           '2': 'Warn',               '3': '12 Hour Ban', '4': '36 Hour Ban'},
                        {"name": 'Self Supply',                  '1': 'Warn',                           '2': 'Warn',               '3': '12 Hour Ban', '4': '36 Hour Ban'},
                        {"name": 'Battering Ram Abuse',          '1': 'Warn + Kick',                    '2': '1 Day Ban',          '3': '5 Day Ban',   '4': '2 Week Ban'}],

                "Chat": [{"name": 'Mic / Chat Spamming',    '1': 'Warn',   '2': 'Gag / Mute + Warn',    '3': 'Kick + Warn', '4': '36 Hour Ban'},
                        {"name": 'Minor Job Abuse',         '1': 'Warn',   '2': 'Warn',                 '3': '12 Hour Ban', '4': '36 Hour Ban'},
                        {"name": 'Self Supply',             '1': 'Warn',   '2': 'Gag / Mute + Warn',    '3': '36 Hour Ban', '4': '3 Day Ban'},
                        {"name": 'Battering Ram Abuse',     '1': 'Warn',   '2': 'Kick + Warn',          '3': '1 Day Ban',   '4': '3 Day Ban'}],

                "General": [{"name": 'NLR',                        '1': 'Warn',            '2': 'Warn',            '3': '12 Hour Ban', '4': '36 Hour Ban'},
                           {"name": 'RDA',                         '1': 'Warn',            '2': 'Warn',            '3': '36 Hour Ban', '4': '3 Day Ban'},
                           {"name": 'RDM / ARDM',                  '1': 'Warn',            '2': 'Warn',            '3': '36 Hour Ban', '4': '3 Day Ban'},
                           {"name": 'Missclick / Crossfire RDM',   '1': 'Verbal Warn',     '2': 'Verbal Warn',     '3': '12 Hour Ban', '4': '1 Day Ban'},
                           {"name": 'Free Spelling',               '1': 'Warn',            '2': 'Warn',            '3': '12 Hour Ban', '4': '36 Hour Ban'},
                           {"name": 'FailRP',                      '1': 'Warn',            '2': 'Warn',            '3': '2 Day Ban',   '4': '4 Day Ban'}],

                "Minge": [{"name": 'Minor Prop Abuse',  '1': 'Warn', '2': '2 Day Ban',      '3': '4 Day Ban',      '4': '1 Week Ban'},
                        {"name": 'Text Screen Abuse',   '1': 'Warn', '2': '12 Hour Ban',    '3': '36 Hour Ban',    '4': '5 Day Ban'},
                        {"name": 'Minge',               '1': 'Warn', '2': '12 Hour Ban',    '3': '36 Hour Ban',    '4': '5 Day Ban'}],

                "Chat (Major)": [{"name": 'Web/Server Advertising',   '1': '2 Week Ban', '2': 'Perm Ban',       '3': 'Perm Ban',       '4': 'Perm Ban'},
                                {"name": 'Major Impersonation',       '1': '5 Day Ban',  '2': '8 Day Ban',      '3': '2 Week Ban',     '4': '3 Week Ban'},
                                {"name": 'Major Discrimination',      '1': '5 Day Ban',  '2': '8 Day Ban',      '3': '2 Week Ban',     '4': '3 Week Ban'},
                                {"name": 'Endorsing Suicide',         '1': '10 Day Ban', '2': '12 Week Ban',    '3': 'Perm Ban',       '4': 'Perm Ban'}],

                "General (Major)": [{"name": 'NITRP',               '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Mass NLR',            '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Mass RDA',            '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Mass RDM/ARDM',       '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Mass Minge',          '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Major Job Abuse',     '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Major Prop Abuse',    '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'LTAP',                '1': '5 Day Ban', '2': '8 Day Ban', '3': '2 Week Ban', '4': '3 Week Ban'},
                                    {"name": 'Scamming',            '1': 'Perm Ban',  '2': 'Perm Ban',  '3': 'Perm Ban',   '4': 'Perm Ban'}]

            }
    topics = ["Base", "Jobs", "Chat", "General", "Minge", "Chat (Major)", "General (Major)", "Staff", ]

    frame3 = ScrollableFrame(Page1)

    yPos = 0

    for i3, topic in enumerate(topics):
        block_frame = Frame(frame3.scrollable_frame, bd=2, bg="#6fa8dc", width=10)
        block_frame.grid(row=yPos, column=0, sticky="nw", pady=(10,0))

        L0 = Label(block_frame, text=str(topic), relief=RAISED, width=25, bd=1, bg="#6fa8dc")
        L0.grid(row=yPos, column=0, sticky="n")

        L1 = Label(block_frame, text="1st Offence", relief=RAISED, width=25, bd=1, bg="#6fa8dc")
        L1.grid(row=yPos, column=1, sticky="n")
        L2 = Label(block_frame, text="2st Offence", relief=RAISED, width=16, bd=1, bg="#6fa8dc")
        L2.grid(row=yPos, column=2, sticky="n")
        L3 = Label(block_frame, text="3st Offence", relief=RAISED, width=16, bd=1, bg="#6fa8dc")
        L3.grid(row=yPos, column=3, sticky="n")
        L4 = Label(block_frame, text="4st Offence +", relief=RAISED, width=16, bd=1, bg="#6fa8dc")
        L4.grid(row=yPos, column=4, sticky="n")
        # yPos += 1

        try:
            for i, item in enumerate(offences[topic], start=yPos+1):
                block_frame = Frame(frame3.scrollable_frame, bd=2, bg=("#f4cccc" if i % 2 else "#e06666"), width=10)
                block_frame.grid(row=i, column=0, sticky="nw")


                for i2, key in enumerate(item.keys(), start=1):
                    Width = (25 if key in ["1", "name"] else 16)
                    L5 = Label(block_frame, text=item[key], relief=RAISED, width=Width, bd=1, bg=("#f4cccc" if i % 2 else "#e06666"))
                    L5.grid(row=i, column=i2, sticky="n")
                    yPos += 1
        except Exception as e:
            yPos += 1
            print(e)

    frame3.pack(fill="both")

    Page1.columnconfigure(0, weight=1)
    Page1.columnconfigure(1, weight=1)
    Page1.rowconfigure(1, weight=1)

def main_app(frame=None):
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


    F2 = Frame(Page1, height=frame_height2, width=frame_width, bg="#E9E9E9", relief="raise")
    F2.grid(row=1,column=0)
    F2.grid_propagate(0)

    myFont2 = Font(family="Times New Roman", size=14)
    width2 = 14
    BG = "light green"
    FG = "black"

    B3 = Button(F2, text="Ban Appeal", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=15"), bd=2)
    B3.grid(row=0,column=0)

    B4 = Button(F2, text="Warn Appeal", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=25"), bd=2)
    B4.grid(row=0,column=1)

    B5 = Button(F2, text="Staff Applications", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=14"), bd=2)
    B5.grid(row=0,column=2)


    B6 = Button(F2, text="Player Reports", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=16"), bd=2)
    B6.grid(row=1,column=0)

    B7 = Button(F2, text="Rules", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/showthread.php?tid=6355"), bd=2)
    B7.grid(row=1,column=1)

    B8 = Button(F2, text="Job Rules", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/showthread.php?tid=8627"), bd=2)
    B8.grid(row=1,column=2)


    B9 = Button(F2, text="Staff Reports", font=myFont2, width=width2, height=1, fg=FG, bg=BG, command=partial(WB_open,"https://elitelupus.com/forums/forumdisplay.php?fid=17"), bd=2)
    B9.grid(row=2,column=0)


    B10 = Button(F2, text="Punishments", font=myFont2, width=width2, height=1, fg=FG, bg="red", command=punishment_app, bd=2)
    B10.grid(row=2,column=1)

    B11 = Button(F2, text="Punishments Web", font=myFont2, width=width2, height=1, fg=FG, bg="red", command=partial(WB_open, "https://docs.google.com/spreadsheets/d/14vFQx_pY6J_2eEEUBL3zQiULi0XGN9JMxW3JR_CLCtg/edit#gid=0"), bd=2)
    B11.grid(row=2,column=2)




    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
