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

import markdown
from tkinterweb import HtmlFrame #import the HTML browser


import tkinter as tk
help_data = {}
help_data[0] = ("Rules", "", "True")
help_data[1] = ("  - General Server Rules", "test", "False")
help_data[2] = ("  - Building Rules", "test", "False")
help_data[3] = ("  - Raiding", "test", "False")
help_data[4] = ("  - Basing", "test", "False")
help_data[5] = ("  - Mugging", "test", "False")
help_data[6] = ("  - Kidnapping", "test", "False")
help_data[7] = ("  - Clans", "test", "False")
help_data[8] = ("  - Purge", "test", "False")
help_data[9] = ("  - Refunds", "test", "False")


help_data[10] = ("Job-Specific Rules", "", "True")
help_data[11] = ("  - Law Enforcement", "<h1>Law Enforcement</h1><p>J1.1 Don’t use lethal force unless necessary.</p><p>J1.2 You’re only allowed to raid a base if you suspect illegal activity.</p><p>J1.3 Do not arrest other Law Enforcement.</p><p>J1.4 (a) As the President you may not make laws that target specific groups, E.g. 'Above Tier 1 is AOS' or 'All thieves are AOS'</p><p>J1.4 (b.) As the President you may not make laws that ruin the player experience, E.g. 'Jaywalking is AOS'</p><p>J1.5 Law enforcement are not allowed to be corrupt.</p><p>J1.6 Printers are illegal by default unless stated otherwise.</p><p>J1.7 Law 'Guns out is AOS' Must include with no gun license.</p><p>J1.8 As President you are not allowed to put KOS with laws. ( E.g. KOS if guns out in public)</p><p>J1.9 You cannot defend or be defended by your clan but you may defend other law enforcement.</p><p>J1.10 You may not enter a base without a warrant.</p>", "False")
help_data[12] = ("  - Hitman", "<h1>Hitman</h1><p>J2.1 You’re not allowed to ask someone if they can put a hit on a specific player.</p><p>J2.2 You’re not allowed to work/base with anyone.</p><p>J2.3 You're not allowed to raid, unless you have a hit on the player then you may break in solely to achieve the hit (No stealing etc).</p><p>J2.4 You're not allowed to kill your hit if the person is building.</p><p>J2.5 You're not allowed to assist a hitman and you can't clan defend them and they can't clan defend others.</p>", "False")
help_data[13] = ("  - Guards", "<h1>Guards</h1><p>J3.1 You're not able to allow a criminal into the base.</p>", "False")
help_data[14] = ("  - Gun Dealers", "<h1>Gun Dealers</h1><p>J4.1 You must have a gun store open.</p><p>J4.2 Self-supplying is not allowed. (spawning yourself multiple shipments and changing job/refusing to sell to others)</p><p>J4.3 Gun shelves must be fully visible. (I.e. You cannot cover prices/guns.)</p>", "False")
help_data[15] = ("  - DJ", "<h1>DJ</h1><p>J5.1 As a DJ you are only allowed to play music in your own building/house/DJ Booth.</p><p>J5.2 You may only make one DJ booth as a DJ, do not make it in the middle of a street or interfere with someone's house/base.</p><p>J5.3 Do not play any discriminatory music (refer to 1.4) and not inappropiate stuff (E.g.: NSFW noises etc.)</p>", "False")
help_data[16] = ("  - Miners", "<h1>Miners</h1><p>J6.1 Auto Clickers are only permitted to be used for mining.</p><p>J6.2 AFK mining is allowed. </p><p>J6.3 You must be either a miner or a citizen to mine.</p>", "False")
help_data[17] = ("  - Luke Skywalker/Darth Vader", "<h1>Luke Skywalker/Darth Vader</h1><p>J7.1 Both jobs can kill each other on sight.(Watch out for others) </p>", "False")
help_data[17] = ("  - Harry Potter/Voldemort", "<h1>Harry Potter/Voldemort</h1><p>J8.1 Both jobs can kill each other on sight.(Watch out for others)</p>", "False")
help_data[18] = ("  - Bank Rules", "<h1>Bank Rules</h1><p>J9.1 Police cannot raid the bank or steal money bags, this is FailRP.</p><p>J9.2 Only the Bank Manager and hired Security Guards are allowed to build in the bank.</p><p>J9.3 The Bank Manager is allowed to store printers for a certain price.</p><p>J9.4 Printers in the bank are not illegal.</p><p>J9.5 If you're in possession of stolen money bags, police can KOS/AOS you.</p><p>J9.6 You are KOS/AOS when interacting with corrupt bankers by Law Enforcement and jobs that are allowed to steal.</p><p>J9.7 You are not allowed to base on/near the corrupt banker (within 10 meters).</p><p>J9.8 Any non-police found in the bank vault are KOS/AOS by government officials (Bank Manager can decide whether to make past lobby KOS/AOS). This also applies to the entire police department, excluding the front lobby.</p>", "False")
help_data[19] = ("  - Job Rules", "<h1>Job Rules</h1><p>J10.1 Every Job can have Blade Printers.</p>", "False")


help_data[20] = ("Job-Actions", "", "True")
help_data[21] = ("      - Citizen", "<h1>Citizen</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (But with no raidables.)</p><p>Can have printers: No</p>", "False")
help_data[22] = ("      - Miner/Retro Miner", "<h1>Miner/Retro Miner</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: No</p><p>Can have printers: No</p>", "False")
help_data[23] = ("      - City Worker", "<h1>City Worker</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: No</p><p>Can have printers: No</p>", "False")
help_data[24] = ("      - Pharmacist", "<h1>Pharmacist</h1><p>Can raid: Yes</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: Yes</p><p>Can base: Yes</p><p>Can have printers: No</p>", "False")
help_data[25] = ("      - Alchemist", "<h1>Alchemist</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes</p><p>Can have printers: No</p>", "False")
help_data[26] = ("      - DJ", "<h1>DJ</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only a DJ stand/house.)</p><p>Can have printers: No</p>", "False")
help_data[27] = ("      - Casino Owner", "<h1>Casino Owner</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only in the casino.)</p><p>Can have printers: No</p>", "False")
help_data[28] = ("      - Hobo King", "<h1>Hobo King</h1><p>Can raid: No</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: No</p><p>Can base: Yes (Only a Hobo shack which cannot have any raidables or be on the street)</p><p>Can have printers: No</p>", "False")
help_data[29] = ("      - Security Guard", "<h1>Security Guard</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (If hired to protect a base)</p><p>Can have printers: No (Unless hired to protect the bank and the printer is placed in the bank.)</p>", "False")
help_data[30] = ("      - Medic", "<h1>Medic</h1><p>Can raid: Yes (Hired and with 3 or more people)</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Hired and with 3 or more people)</p><p>Can have printers: No </p>", "False")
help_data[31] = ("      - Gun Dealer (And all variants.)", "<h1>Gun Dealer (And all variants.)</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes </p><p>Can have printers: No (Only Bitminers) </p>", "False")
help_data[32] = ("  - Law Enforcement", "", "True")
help_data[33] = ("      - President Donald J Trump", "<h1>President Donald J Trump</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only in the PD.)</p><p>Can have printers: No</p>", "False")
help_data[34] = ("      - All Police, Swat And Secret Service", "<h1>All Police, Swat And Secret Service</h1><p>Can raid: Yes (With a warrant.)</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only with the president in PD.)</p><p>Can have printers: No</p>", "False")
help_data[35] = ("      - Luke Skywalker", "<h1>Luke Skywalker</h1><p>Can raid: Yes (With a warrant and with SWAT.)</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only with the president in PD.)</p><p>Can have printers: No</p>", "False")
help_data[36] = ("      - Bank Manager", "<h1>Bank Manager</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: Yes (Only in the bank.)</p><p>Can have printers: Yes (Only in the bank.)</p>", "False")
help_data[37] = ("  - Criminals", "", "True")
help_data[38] = ("      - Thief  (all thief variants)", "<h1>Thief  (all thief variants)</h1><p>an raid: Yes</p><p>an steal: Yes</p><p>an mug: Yes</p><p>an kidnap: No (Anime Thief Ultimate and Platinum can)</p><p>an base: Yes</p><p>an have printers: Yes</p>", "False")
help_data[39] = ("      - Weed Grower (all variants)", "<h1>Weed Grower (all variants)</h1><p>Can raid: No(Op can)</p><p>Can steal: No(Op can)</p><p>Can mug: No(Op can)</p><p>Can kidnap: No</p><p>Can base: Yes (Op can)</p><p>Can have printers: Yes</p>", "False")
help_data[40] = ("      - Drug Cook (all Drug Cook variants)", "<h1>Drug Cook (all Drug Cook variants)</h1><p>Can raid: No (Pro and Ultimate can)</p><p>Can steal: No (Ultimate can)</p><p>Can mug: No (Ultimate can)</p><p>Can kidnap: No (Ultimate can)</p><p>Can base: Yes (Drug Lab must be in base)</p><p>Can have printers: Yes</p>", "False")
help_data[41] = ("      - Wizard", "<h1>Wizard</h1><p>Can raid: Yes</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: Yes</p><p>Can base: Yes</p><p>Can have printers: Yes</p>", "False")
help_data[42] = ("      - Harry Potter and Voldemort", "<h1>Harry Potter and Voldemort</h1><p>Can raid: Yes</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: No</p><p>Can base: Yes but not with each other</p><p>Can have printers: Yes</p>", "False")
help_data[43] = ("      - Kidnapper", "<h1>Kidnapper</h1><p>Can raid: No</p><p>Can steal: No</p><p>Can mug: Yes</p><p>Can kidnap: Yes</p><p>Can base: Yes</p><p>Can have printers: Yes </p>", "False")
help_data[44] = ("      - Hitman (all variants)", "<h1>Hitman (all variants)</h1><p>Can raid: Yes (Only to achieve a hit.)</p><p>Can steal: No</p><p>Can mug: No</p><p>Can kidnap: No</p><p>Can base: No </p><p>Can have printers: No</p>", "False")
help_data[45] = ("      - Darth Vader", "<h1>Darth Vader</h1><p>Can raid: Yes</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: No</p><p>Can base: Yes</p><p>Can have printers: Yes</p>", "False")
help_data[46] = ("  - Gangs", "", "True")
help_data[47] = ("      - Bloodz/Cripz Leader", "<h1>Bloodz/Cripz Leader</h1><p>Can raid: Yes </p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: Yes</p><p>Can base: Yes but not with each other</p><p>Can have printers: Yes</p>", "False")
help_data[48] = ("      - Bloodz/Cripz Lieutenant", "<h1>Bloodz/Cripz Lieutenant</h1><p>Can raid: Yes (Only with your gang leader.)</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: No</p><p>Can base: Yes (Only with your gang leader.)</p><p>Can have printers: Yes</p>", "False")
help_data[49] = ("      - Bloodz/Cripz Member", """<h1>Bloodz/Cripz Member</h1><p>Can raid: Yes (Only with your gang leader/Lieutenant.)</p><p>Can steal: Yes</p><p>Can mug: Yes</p><p>Can kidnap: No</p><p>Can base: Yes (Only with your gang leader.)</p><p>Can have printers: Yes</p>""", "False")



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

    def disable_item(index, listbox):
        listbox.itemconfig(index, fg="gray")
        ignored_index.append(index)

    def onselect(event):
        listbox = event.widget
        index = int(listbox.curselection()[0])
        if index in ignored_index:
            listbox.selection_clear(index)
        else:
            value = listbox.get(index)

            item = help_data[index]

            markdownText = item[1]
            html = markdown.markdown(markdownText, extensions=['fenced_code', 'codehilite'])
            outputbox.load_html(html) #load a website
            outputbox.add_css((open("codehilite.css", 'r')).read())

    help_page_tk = Toplevel()
    # frame_bottom.configure(bg="#444444" if theme == "DarkTheme" else "#D3D3D3")
    # help_page_tk.configure(bg="#121212" if theme == "DarkTheme" else "#D3D3D3")
    help_page_tk.title("Help Menu")
    help_page_tk.geometry("900x400")
    # help_page_tk.geometry("1200x600")
    help_page_tk.transient(frame)
    help_page_tk.update_idletasks()

    ignored_index = []

    frame_left_width = 15
    frame_left = ttk.Frame(help_page_tk, width=frame_left_width, height=(help_page_tk.winfo_height()))
    frame_left.pack(side='left', fill=BOTH)

    # frame_left.columnconfigure(0, weight=10)
    # frame_left.rowconfigure(0, weight=10)
    frame_left.grid_propagate(False)
    frame_left.update_idletasks()


    Lb1 = Listbox(frame_left, height=(frame_left.winfo_height()))

    for index in help_data.keys():
        item = help_data[index]
        Lb1.insert(index, item[0])

        if item[2] == "True":
            disable_item(index, Lb1)

    Lb1.bind('<<ListboxSelect>>', onselect)


    Lb1.pack()


    frame_right = ttk.Frame(help_page_tk, width=help_page_tk.winfo_width(), height=help_page_tk.winfo_height())
    frame_right.pack(side='right', fill=BOTH)

    frame_right.columnconfigure(0, weight=10)
    frame_right.rowconfigure(0, weight=10)
    frame_right.grid_propagate(False)
    frame_right.update_idletasks()

    outputbox = HtmlFrame(frame_right, style="custom.TFrame", height=(frame_right.winfo_height()), width=(help_page_tk.winfo_width()-frame_left_width)) #create the HTML browser
    outputbox.load_html("<h1>Select an option!</h1>") #load a website
    outputbox.add_css((open("codehilite.css", 'r')).read())
    outputbox.set_zoom(0.8)
    outputbox.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window



    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
