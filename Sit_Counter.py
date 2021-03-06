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
import platform
import sys
import webbrowser
import threading
import time

filepath = 'refunds.db'
conn = sqlite3.connect(filepath)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Stats(ID INT, Name TEXT, Detail RAEL)''')
c.execute('''CREATE TABLE IF NOT EXISTS Commands(ID INT, Name TEXT, Detail RAEL)''')


def main_app(frame=None, theme="DarkTheme"):
    if frame == None:
        Page1 = Tk()
        Page1.title("Elitelupus Refund Template Maker")
    else:
        Page1 = frame

    def Add_count():
        c.execute("SELECT Detail FROM Stats")
        Current = (c.fetchall()[0][0])

        if Current >= 0:
            New = Current + 1
        else:
            New = 1

        Stats.set(New)

        c.execute("UPDATE Stats SET Detail=? WHERE ID=1",(New,))
        conn.commit()

    def Remove_count():
        c.execute("SELECT Detail FROM Stats")
        Current = (c.fetchall()[0][0])

        if Current >= 0:
            New = Current - 1
        else:
            New = 0

        Stats.set(New)

        c.execute("UPDATE Stats SET Detail=? WHERE ID=1",(New,))
        conn.commit()

    def Add_ticket_count():
        c.execute("SELECT Detail FROM Stats")
        Current = (c.fetchall()[1][0])

        if Current >= 0:
            New = Current + 1
        else:
            New = 1

        Stats2.set(New)

        c.execute("UPDATE Stats SET Detail=? WHERE ID=2",(New,))
        conn.commit()

    def Remove_ticket_count():
        c.execute("SELECT Detail FROM Stats")
        Current = (c.fetchall()[1][0])

        if Current >= 0:
            New = Current - 1
        else:
            New = 0

        Stats2.set(New)

        c.execute("UPDATE Stats SET Detail=? WHERE ID=2",(New,))
        conn.commit()


    frame_width = 445
    frame_height1 = 100
    frame_height2 = 120

    F1 = Page1

    myFont = Font(family="Times New Roman", size=20)

    label1 = ttk.Label(F1, text='Total Sits: ')
    label1.grid(row=0,column=0,sticky='e', pady=(0, 5))
    label1.configure(font=myFont)

    Stats = StringVar()
    label2 = ttk.Label(F1, textvariable=Stats)
    label2.grid(row=0,column=1,sticky='w', pady=(0, 5))
    label2.configure(font=myFont)

    try:
        c.execute("SELECT Detail FROM Stats")
        count = (c.fetchall()[0][0])
        Stats.set(count)
    except:
        c.execute('''INSERT INTO Stats(ID, Name, Detail) VALUES(?, ?, ?)''',(1, "count", 0))
        conn.commit()
        count = 0
        Stats.set(count)

    B1 = ttk.Button(F1, text="Add Sit", width=12, command=Add_count)
    B1.grid(row=1,column=0)

    B2 = ttk.Button(F1, text="Remove Sit", width=12, command=Remove_count)
    B2.grid(row=1,column=1)


    label3 = ttk.Label(F1, text='Total Tickets: ')
    label3.grid(row=2,column=0,sticky='e', pady=(0, 5))
    label3.configure(font=myFont)

    Stats2 = StringVar()
    label4 = ttk.Label(F1, textvariable=Stats2)
    label4.grid(row=2,column=1,sticky='w', pady=(0, 5))
    label4.configure(font=myFont)

    try:
        c.execute("SELECT Detail FROM Stats")
        count = (c.fetchall()[1][0])
        Stats2.set(count)
    except:
        c.execute('''INSERT INTO Stats(ID, Name, Detail) VALUES(?, ?, ?)''',(2, "ticket count", 0))
        conn.commit()
        count = 0
        Stats2.set(count)

    B3 = ttk.Button(F1, text="Add Ticket", width=12, command=Add_ticket_count)
    B3.grid(row=3,column=0)

    B4 = ttk.Button(F1, text="Remove Ticket", width=12, command=Remove_ticket_count)
    B4.grid(row=3,column=1)


    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
