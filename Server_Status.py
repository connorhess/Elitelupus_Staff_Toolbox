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
import requests

# https://python-valve.readthedocs.io/en/latest/rcon.html
import valve.source as source
# import valve.source.a2s as a2s
import a2s
import Staff_Distribution as staffd
import valve.source.master_server as master_server

import Elitelupus_ban_search as ebs

import tkinter as tk

global id_s, checked
checked = False
id_s = 0

elite_server_1 = ("194.69.160.33", 27083)
elite_server_2 = ("193.243.190.12", 27046)

colors = {
    "Management": "#990000",
    "Staff Manager": "#F04000",
    "Assistant SM": "#8900F0",
    "Snr Admin": "#d207d3",
    "Admin": "#FA1E8A",
    "Snr Moderator": "#15c000",
    "Moderator": "#4a86e8",
    "Snr Operator": "#38761d",
    "Operator": "#93c47d",
    "T-Staff": "#b6d7a8",
    "user": "grey"
}

players_s1 = {}
for player in a2s.players(elite_server_1):
    print(player)
    players_s1.update({player.name: (player.score, int(player.duration))})

players_s2 = {}
for player in a2s.players(elite_server_2):
    print(player)
    players_s2.update({player.name: (player.score, int(player.duration))})



def format_seconds_to_time(seconds):
    try:
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60

        days = int(seconds // seconds_in_day)
        hours = int((seconds - (days * seconds_in_day)) // seconds_in_hour)
        minutes =  int((seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute)

        string = ""

        if seconds == 0:
            string += "0"

        if days != 0:
            string += f"{days} Days, "

        if hours != 0 and minutes == 0:
            string += f"{hours} Hours, "
        elif hours != 0 and minutes != 0:
            string += f"{hours} Hours, and "

        if minutes != 0:
            string += f"{minutes} Minutes"

        if minutes == 0 and hours == 0 and minutes == 0:
            string += f"{int(seconds)} Seconds"


        return string
    except Exception as e:
        print(f"Error [Server_Stats][1]: {e}")
        return "error"



class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        container.update()
        canvas = tk.Canvas(self, height=container.winfo_height())
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, height=container.winfo_height())

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        # canvas.grid(row=0, column=0, sticky="w")
        scrollbar.pack(side="right", fill="y")
        # scrollbar.grid(row=0, column=1, sticky="w")


def create_tree(master, columns=("Symbol", "Channel", "Ticket", "Time", "Volume", "Price", "Profit"), total_width=520, parent_size=0):
    tree_list = ttk.Treeview(master)
    tree_list["columns"] = columns

    tree_list.column("#0", width=parent_size, minwidth=parent_size)
    tree_list.heading("#0", text="#")

    width = int(total_width / len(columns))
    for column in columns:
        tree_list.column(str(column), anchor='w', width=width)
        tree_list.heading(str(column), text=str(column), anchor='w')

    return tree_list


def main_app(frame=None, theme="DarkTheme"):
    if frame == None:
        Page1 = Tk()
        Page1.title("Elitelupus Server Monitor")
        # Page1.geometry("720x296")
        # Page1.resizable(False, False)
    else:
        Page1 = frame


    Stats1 = StringVar()
    label1 = ttk.Label(Page1, textvariable=Stats1)
    label1.grid(row=1,column=0)

    Trade_list = create_tree(Page1, columns=("Name", "Score", "Rank", "Duration"))
    Trade_list['height'] = 6
    Trade_list.grid(row=2, column=0, sticky="w")


    Stats2 = StringVar()
    label2 = ttk.Label(Page1, textvariable=Stats2)
    label2.grid(row=3,column=0)

    Trade_list2 = create_tree(Page1, columns=("Name", "Score", "Rank", "Duration"))
    Trade_list2['height'] = 6
    Trade_list2.grid(row=4, column=0, sticky="w")


    def update():
        global id_s, checked
        while True:

            if checked == False:
                staff_list, staff_list_inv = staffd.get_staff_list()
                checked = True


            # staff_list_1, staff_list_2 = staffd.get_staff_server(staff_list=staff_list)

            try:
                info = a2s.info(elite_server_1)
                Stats1.set(f"{info.player_count}/{info.max_players} {info.server_name}")

                for i in Trade_list.get_children():
                    Trade_list.delete(i)

                players_s1 = {}
                for player in a2s.players(elite_server_1):
                    try:
                        players_s1.update({player.name: (player.score, format_seconds_to_time(int(player.duration)))})
                    except Exception as e:
                        print(f"Error [Server_Stats][4]: {e}")
                        players_s1.update({"[Name Error]": (player.score, format_seconds_to_time(int(player.duration)))})


                for player in players_s1.keys():
                    try:
                        id_s += 1
                        rank_val = staff_list_inv[player]['Rank'] if player in staff_list_inv.keys() else "user"
                        Item = (player, players_s1[player][0], rank_val, players_s1[player][1])
                        Trade_list.insert("", index=0, iid=id_s, text="", values=Item, tag=rank_val.replace(' ', '_'))
                    except Exception as e:
                        print(f"Error [Server_Stats][4]: {e}")
            except Exception as e:
                print(f"Error [Server_Stats][2]: {e}")
                Stats1.set(f"Server 1 Crashed or code is unable to get data")
                for i in Trade_list.get_children():
                    Trade_list.delete(i)



            try:
                info = a2s.info(elite_server_2)
                Stats2.set(f"{info.player_count}/{info.max_players} {info.server_name}")

                for i in Trade_list2.get_children():
                    Trade_list2.delete(i)

                players_s2 = {}
                for player in a2s.players(elite_server_2):
                    try:
                        players_s2.update({player.name: (player.score, format_seconds_to_time(int(player.duration)))})
                    except Exception as e:
                        print(f"Error [Server_Stats][4]: {e}")
                        players_s2.update({"[Name Error]": (player.score, format_seconds_to_time(int(player.duration)))})

                for player in players_s2.keys():
                    try:
                        id_s += 1
                        rank_val = staff_list_inv[player]['Rank'] if player in staff_list_inv.keys() else "user"
                        Item = (player, players_s2[player][0], rank_val, players_s2[player][1])
                        Trade_list2.insert("", index=0, iid=id_s, text="", values=Item, tag=rank_val.replace(' ', '_'))
                    except Exception as e:
                        print(f"Error [Server_Stats][4]: {e}")
            except Exception as e:
                print(f"Error [Server_Stats][3]: {e}")
                Stats1.set(f"Server 1 Crashed or code is unable to get data")
                for i in Trade_list.get_children():
                    Trade_list.delete(i)

            for rank in colors.keys():
                color = colors[rank]
                Trade_list.tag_configure(rank.replace(' ', '_'), background=color)
                Trade_list2.tag_configure(rank.replace(' ', '_'), background=color)


            time.sleep(30)


    def OnDoubleClickServer1(event):
        item = tree.selection()[0]
        print("you clicked on", tree.item(item,"text"))

    def OnDoubleClickServer2(event):
        item = tree.selection()[0]
        print("you clicked on", tree.item(item,"text"))

    Trade_list.bind("<Double-1>", OnDoubleClickServer1)
    Trade_list2.bind("<Double-1>", OnDoubleClickServer2)

    thread = threading.Thread(target=update)
    thread.setDaemon(True)
    thread.start()


    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
