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
import valve.source.master_server as master_server

import Elitelupus_ban_search as ebs

import tkinter as tk

global id_s, checked
id_s = 0
checked = False

sheet_id = "1SSn3GXggr84dOYfQZzeHiRI0B1vaDkGynUyYHWfXIBo"
sheet_name = "Roster"
public_staff_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

elite_server_1 = ("194.69.160.33", 27083)
elite_server_2 = ("193.243.190.12", 27046)

colors = {
    "Manager": "#990000",
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

# df = pandas.read_csv(public_staff_url)
# print(df)

def get_staff_list():
    staff_list = {}
    staff_list_inv = {}
    data = requests.get(public_staff_url)
    data = (data.content).decode('utf-8')
    data = data.split('\n')

    for row in data:
        new_data = row.split(',')
        # print(new_data)
        if "\"Rank\"" not in new_data:
            steam_id = new_data[5].replace("\"", '').strip()

            steam_id = SteamID(steam_id)
            # print(steam_id)

            steam_name = new_data[4].replace("\"", '')
                # print(new_data[2].replace("\"", ''), steam_id)
            # print(steam_name)
            staff_list.update({new_data[4].replace("\"", ''): {"Server": None, "Steam_Name": steam_name, "Name": new_data[4].replace("\"", ''), "Rank": new_data[1].replace("\"", '').strip(), "SteamID": steam_id, "Discord ID": new_data[6].replace("\"", '')}})
            staff_list_inv.update({steam_name: {"Server": None, "Steam_Name": steam_name, "Name": new_data[4].replace("\"", ''), "Rank": new_data[1].replace("\"", '').strip(), "SteamID": steam_id, "Discord ID": new_data[6].replace("\"", '')}})

            # time.sleep(1)

    return (staff_list, staff_list_inv)

def get_staff_server(staff_list):
    players_s1 = {}
    for player in a2s.players(elite_server_1):
        players_s1.update({player.name: (player.score, int(player.duration))})

    players_s2 = {}
    for player in a2s.players(elite_server_2):
        players_s2.update({player.name: (player.score, int(player.duration))})

    server_1 = []
    server_2 = []

    for user in staff_list.keys():
        user = staff_list[user]
        if user['Steam_Name'] != None:
            # print(user['Name'], ":", user['Steam_Name'])
            if players_s1.get(user['Steam_Name']) != None:
                # print(user['Name'], "is on server 1")
                staff_list[user['Name']].update({"Server": 1})
                server_1.append(user)

            elif players_s2.get(user['Steam_Name']) != None:
                # print(user['Name'], "is on server 2")
                staff_list[user['Name']].update({"Server": 2})
                server_2.append(user)

    return (server_1, server_2)

def get_users_server(steamid="STEAM_0:1:526199909"):
    steam_profile = ebs.get_steam_profile(steam_id=steamid, mod=True)
    try:
        steam_name = steam_profile['name']

        players_s1 = {}
        for player in a2s.players(elite_server_1):
            players_s1.update({player.name: (player.score, int(player.duration))})

        players_s2 = {}
        for player in a2s.players(elite_server_2):
            players_s2.update({player.name: (player.score, int(player.duration))})

        if players_s1.get(steam_name) != None:
            return 1

        elif players_s2.get(steam_name) != None:
            return 2

        else:
            return None

    except Exception as e:
        print(f"Error [Staff_Distribution][1]: {e}")
        return None

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
        style = ttk.Style(Page1)
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
        style.theme_use("DarkTheme")

    else:
        Page1 = frame


    Stats1 = StringVar()
    label1 = ttk.Label(Page1, textvariable=Stats1)
    label1.grid(row=1,column=0)


    Trade_list3 = create_tree(Page1, columns=("Rank", "Name", "SteamID"))
    Trade_list3['height'] = 6
    Trade_list3.grid(row=2, column=0, sticky="w")


    Stats2 = StringVar()
    label2 = ttk.Label(Page1, textvariable=Stats2)
    label2.grid(row=3,column=0)

    Trade_list4 = create_tree(Page1, columns=("Rank", "Name", "SteamID"))
    Trade_list4['height'] = 6
    Trade_list4.grid(row=4, column=0, sticky="w")


    def update():
        global id_s, checked
        while True:

            try:

                for i in Trade_list3.get_children():
                    Trade_list3.delete(i)

                for i in Trade_list4.get_children():
                    Trade_list4.delete(i)

                if checked == False:
                    staff_list, staff_list_inv = get_staff_list()
                    checked = True

                server_1, server_2 = get_staff_server(staff_list=staff_list)

                for player in server_1:
                    id_s += 1
                    Item = (player['Rank'], player['Name'], player['SteamID'])
                    Trade_list3.insert("", index=0, iid=id_s, text="", values=Item, tag=player['Rank'].replace(' ', '_'))

                for player in server_2:
                    id_s += 1
                    Item = (player['Rank'], player['Name'], player['SteamID'])
                    Trade_list4.insert("", index=0, iid=id_s, text="", values=Item, tag=player['Rank'].replace(' ', '_'))

                # for player in staff_list.keys():
                #     player = staff_list[player]
                #     id_s += 1
                #     Item = (player['Rank'], player['Name'], player['SteamID'])
                #     Trade_list4.insert("", index=0, iid=id_s, text="", values=Item, tag=player['Rank'].replace(' ', '_'))


                for rank in colors.keys():
                    color = colors[rank]
                    Trade_list3.tag_configure(rank.replace(' ', '_'), background=color)
                    Trade_list4.tag_configure(rank.replace(' ', '_'), background=color)


                info = a2s.info(elite_server_1)
                Stats1.set(f"{len(server_1)}/{info.player_count}/{info.max_players} {info.server_name}")

                info2 = a2s.info(elite_server_2)
                Stats2.set(f"{len(server_2)}/{info2.player_count}/{info2.max_players} {info2.server_name}")


            except Exception as e:
                print(f"Error [Staff_Distribution][2]: {e}")
                Stats1.set(f"Server has Crashed or code is unable to get data")
                for i in Trade_list3.get_children():
                    Trade_list3.delete(i)

            time.sleep(30)


    thread = threading.Thread(target=update)
    thread.setDaemon(True)
    thread.start()


    if frame == None:
        Page1.mainloop()




if __name__ == '__main__':
    main_app()
