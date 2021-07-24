import requests, json
from steam.steamid import SteamID
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pyperclip
from functools import partial
import sqlite3
import ast
from datetime import datetime, timedelta
import threading
import timeago

def format_elapsed_datetime(time):
    time_now = datetime.utcnow()
    # seconds = (datetime.timestamp(time_now) - datetime.timestamp(time))
    # minutes = seconds / 60
    # hours = minutes / 60
    # days = hours / 24
    # weeks = days / 7
    # months = days / 30
    # years = months / 12

    return (timeago.format(time, time_now))


Elite_search_URL = "https://elitelupus.com/bans/search/"

session = requests.Session()


def get_bans(SteamID_entry="STEAM_0:1:526199909"):
    SteamID_Data = SteamID(SteamID_entry)

    SteamID_2 = SteamID_Data.as_steam2_zero


    payload = {'userSteamId': str(SteamID_2), 'submit': 'Search'}


    headers = {'User-Agent': 'Mozilla/5.0'}

    response = session.post(Elite_search_URL, headers=headers, data=payload)


    # response = requests.post(Elite_search_URL, json=data)

    myhtml = (response.text)
    # print(myhtml)

    text = ''

    for item in myhtml.split("</tbody>"):
        if "<tbody>" in item:
            text += (item [ item.find("<tbody>")+len("</tbody>") : ])

    # print(text)

    data_of_steam = []

    for i, item in enumerate(text.split("</tr>")):
        if "<tr>" in item:
            string_from =  (item [ item.find("<tr>")+len("</tr>") : ])

            data_from = (string_from.replace('</td>', '').split('<td>'))
            try:
                url = data_from[4]
                url = url.replace("<a href='..", "").replace("' type='button' class='btn btn-xs btn-primary'>View</a>", "")
                url = (f"https://elitelupus.com/bans{url}")
                data_of_steam.append({'date': data_from[1], 'name': data_from[2], 'steamid': data_from[3], 'url': url})
            except:
                messagebox.showerror("Error", "User Either has no Bans or does not exist")

    return (data_of_steam)



def get_ban_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

    response = session.get(url, headers=headers)

    myhtml = (response.text)
    text = ''
    for item in myhtml.split("</td>"):
        if "<td>" in item:
            text += (item [ item.find("<td>")+len("</td>") : ]).strip() + "\n"

    data = (text.split('\n'))

    return {'Name when banned': data[0],
            'Current name': data[1],
            'Location': data[2],
            'Steam ID': data[3],
            'Profile': data[4],
            'Time of ban': data[5],
            'Server': data[6],
            'Reason': data[7],
            'Banned by': data[8],
            'Unban time': data[9],
            'Unbanned by': data[10]}


def get_all_bans(SteamID_entry="STEAM_0:1:526199909"):
    bans = (get_bans(SteamID_entry=SteamID_entry))

    ban_data = []
    for ban in bans:
        ban_data.append(get_ban_data(url=ban['url']))

    return ban_data

def main_app(frame=None):
    global result_frame
    if frame == None:
        Main = Tk()
        Main.title("Elitelupus Ban Search")
    else:
        Main = frame

    question_frame = Frame(Main)
    # question_frame.grid(row=0, column=0)
    question_frame.pack(fill="x", side="top")

    ML1 = Label(question_frame, text="SteamID (any)")
    ML1.grid(row=0, column=0, sticky="e")

    ME1 = Entry(question_frame, bd=3)
    ME1.grid(row=0, column=1, sticky="e")

    result_frame = Frame(Main)
    # result_frame.grid(row=1, column=0)
    result_frame.pack(fill="both", side="bottom")

    def search_bans():
        global result_frame
        steam_id = str(ME1.get())
        steam_id = steam_id.strip()
        # resultPage = Toplevel()
        # resultPage.title(f"{steam_id}")
        # resultPage.wm_attributes("-topmost", 1)
        # resultPage.geometry("280x170")
        result_frame.grid_forget()
        result_frame.destroy()

        result_frame = Frame(Main)
        # result_frame.grid(row=1, column=0)
        result_frame.pack(fill="both", side="bottom")
        resultPage = result_frame

        Searching_Label = Label(resultPage, text="Searching...")
        Searching_Label.grid(row=0, column=0)

        result = (get_all_bans(SteamID_entry=steam_id))

        Searching_Label.grid_forget()
        Searching_Label.destroy()

        label_list = {}

        tab = {}
        tabControl = ttk.Notebook(resultPage)
        exclude_list = ["Location", "Profile"]

        for ban in result:
            time_of_ban = ban['Time of ban']
            time_of_ban = datetime.strptime(time_of_ban, '%d-%m-%y %H:%M')

            result_name = format_elapsed_datetime(time_of_ban)
            tab.update({result_name: ttk.Frame(tabControl)})
            tabControl.add(tab[result_name], text=result_name)

            for i, item in enumerate(ban.keys()):
                name = item
                data = ban[item]
                if name not in exclude_list:
                    label_list.update({name: Label(tab[result_name], text=f"{name}: ")})
                    label_list[name].grid(row=i, column=0, sticky="e")

                    label_list.update({(name + "_res"): Label(tab[result_name], text=f"{data}")})
                    label_list[(name + "_res")].grid(row=i, column=1, sticky="w")

            label_list.update({"Time Since": Label(tab[result_name], text="Time Since: ")})
            label_list["Time Since"].grid(row=20, column=0, sticky="e")


            label_list.update({("Time Since" + "_res"): Label(tab[result_name], text=f"{result_name}")})
            label_list[("Time Since" + "_res")].grid(row=20, column=1, sticky="w")
            # app.main_app(frame=tab[name])


        tabControl.grid(row=0, column=0)

    def start_search():
        thread = threading.Thread(target=search_bans)
        thread.setDaemon(True)
        thread.start()

    B5 = Button(question_frame, text="Search", command=start_search)
    B5.grid(row=0, column=2, sticky="e")


    if frame == None:
        Main.mainloop()
    # print(get_all_bans(SteamID_entry="STEAM_0:1:526199909"))





# bans = (get_bans(SteamID_entry="STEAM_0:1:526199909"))

# print(get_ban_data(url=bans[0]['url']))
if __name__ == '__main__':
    main_app()
    # # payload = {'userSteamId': str(SteamID_2), 'submit': 'Search'}

    # headers = {'User-Agent': 'Mozilla/5.0'}
    # # url = "https://elitelupus.com/forums/member.php?action=profile&uid=11849"
    # url = "https://elitelupus.com/forums/member.php"

    # response = session.get(url, headers=headers, params={'action': 'profile', "steamid": 'STEAM_0:1:526199909'})

    # print(response)
    # print(response.text)
    # # print(get_all_bans(SteamID_entry="STEAM_0:1:526199909"))


