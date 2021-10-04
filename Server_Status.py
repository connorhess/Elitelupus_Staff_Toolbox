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

# https://python-valve.readthedocs.io/en/latest/rcon.html
import valve.source as source
# import valve.source.a2s as a2s
import a2s
import valve.source.master_server as master_server


import tkinter as tk

global id_s
id_s = 0

elite_server_1 = ("gmod-drp1-uk.elitelupus.com", 27015)
elite_server_2 = ("gmod-drp2-usa.elitelupus.com", 27015)

players_s1 = {}
for player in a2s.players(elite_server_1):
    players_s1.update({player.name: (player.score, int(player.duration))})

players_s2 = {}
for player in a2s.players(elite_server_2):
    players_s2.update({player.name: (player.score, int(player.duration))})


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
        scrollbar.pack(side="right", fill="y")


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

# def check_for_rdm(server):
#     rdmers = {}

#     players = a2s.players(server)
#     # print("="*60)
#     # print("{score} {name} {duration}".format(**player))
#     for name in user_kills.keys():
#         kills = int(players_s1[name])
#         new_kills = int(player['score']) - kills
#         if new_kills >= 4:
#             pass

#     return rdmers

def main_app(frame=None, theme="DarkTheme"):
    if frame == None:
        Page1 = Tk()
        Page1.title("Elitelupus Refund Template Maker")
    else:
        Page1 = frame

    Stats1 = StringVar()
    label1 = ttk.Label(Page1, textvariable=Stats1)
    label1.grid(row=1,column=0)

    Trade_list = create_tree(Page1, columns=("Name", "Score", "Duration"))
    # Trade_list['height'] = 12
    Trade_list.grid(row=2, column=0, sticky="w")


    Stats2 = StringVar()
    label2 = ttk.Label(Page1, textvariable=Stats2)
    label2.grid(row=3,column=0)

    Trade_list2 = create_tree(Page1, columns=("Name", "Score", "Duration"))
    # Trade_list2['height'] = 12
    Trade_list2.grid(row=4, column=0, sticky="w")






    def update():
        global id_s
        while True:
            info = a2s.info(elite_server_1)
            Stats1.set(f"{info.player_count}/{info.max_players} {info.server_name}")
            print(f"{info.player_count}/{info.max_players} {info.server_name}")

            info = a2s.info(elite_server_2)
            Stats2.set(f"{info.player_count}/{info.max_players} {info.server_name}")
            print(f"{info.player_count}/{info.max_players} {info.server_name}")

            for i in Trade_list.get_children():
                Trade_list.delete(i)
            for i in Trade_list2.get_children():
                Trade_list2.delete(i)

            for i, player in enumerate(players_s1.keys()):
                id_s += 1
                Item = (player, players_s1[player][0], players_s1[player][1])
                Trade_list.insert("", index=0, iid=id_s, text="", values=Item, tag=id_s)

            for player in players_s2.keys():
                id_s += 1
                Item = (player, players_s2[player][0], players_s2[player][1])
                Trade_list2.insert("", index=0, iid=id_s, text="", values=Item, tag=id_s)


            time.sleep(60)


    thread = threading.Thread(target=update)
    thread.setDaemon(True)
    thread.start()


    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
