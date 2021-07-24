from steam.steamid import SteamID
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pyperclip
from functools import partial
import sqlite3
import ast
from tkcalendar import Calendar

# pyperclip.copy('The text to be copied to the clipboard.')
# spam = pyperclip.paste()

def steam_64(id="STEAM_0:0:572644049"):
    SteamID_Data = SteamID(id)
    SteamID_2 = SteamID_Data.as_64
    return str(SteamID_2)

refunds = {}
refund_counter = 0
refund_data = {}


def refund_app(frame=None):
    global refund_data, refunds, refund_counter
    if frame == None:
        Main = Tk()
        Main.title("Elitelupus Refund Template Maker")
    else:
        Main = frame

    filepath = 'refunds.db'
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS refunds(Id TEXT, Data TEXT)''')

    topFrame = Frame(Main)
    topFrame.grid(row=0, column=0, sticky="w")


    ML1 = Label(topFrame, text="Ticket Number")
    ML1.grid(row=0, column=0, sticky="e")

    ME1 = Entry(topFrame, bd=3)
    ME1.grid(row=0, column=1, sticky="e")

    ME1.delete(0,END)
    ME1.insert(0,"ticket-")


    middleFrame = Frame(Main)
    middleFrame.grid(row=1, column=0, sticky="nw")

    middleRightFrame = Frame(middleFrame)
    middleRightFrame.grid(row=0, column=0, sticky="nw")

    middleLeftFrame = Frame(middleFrame)
    middleLeftFrame.grid(row=0, column=1, sticky="nw")
    ML2 = Label(middleLeftFrame, text="Actions:")
    ML2.grid(row=0, column=0, sticky="w")


    ML1 = Label(middleRightFrame, text="Tickets:")
    ML1.grid(row=0, column=0, sticky="w")

    Lb1 = Listbox(middleRightFrame, width=20, height=10)

    c.execute("SELECT * FROM refunds")
    for row in c.fetchall():
        refund_id = row[0]
        database_data = ast.literal_eval(row[1])
        refund_data.update({refund_id: database_data})
        Lb1.insert(1, refund_id)

    def save_data(refund_id):
        c.execute('''DELETE FROM refunds WHERE Id=?''',(refund_id,))
        c.execute('''INSERT INTO refunds(Id, Data) VALUES(?, ?)''',(refund_id, str(refund_data[refund_id])))
        conn.commit()

    def rename_data(old_refund_id, new_refund_id):
        c.execute("UPDATE refunds SET Id=? WHERE Id = ?",(new_refund_id,old_refund_id))
        conn.commit()

    def delete_data(refund_id):
        c.execute('''DELETE FROM refunds WHERE Id=?''',(refund_id,))
        conn.commit()

    def copy_question_to_cb():
        pyperclip.copy(f"""Please Send Your:
IGN:
SteamID64:
Items Lost:
Reason:
Evidence:
""")

    def new_refund(open_data=None):
        print(open_data)
        global refund_data, refunds, refund_counter
        ME1_data = str(ME1.get())

        ME1.delete(0,END)
        ME1.insert(0,"ticket-")
        data = False

        if len(ME1_data.replace('ticket-', '').replace('refund-', '').strip()) == 0 and open_data == None:
            return ""

        if open_data == None:
            refund_id = ME1_data
            Lb1.insert(1, refund_id)
        else:
            refund_id = open_data

        print(refund_id)

        if refund_data.get(refund_id) == None:
            refund_data.update({refund_id: {}})


        refunds.update({refund_id: Toplevel()})
        refunds[refund_id].title(f"{refund_id}")
        refunds[refund_id].geometry("280x210")
        refunds[refund_id].wm_attributes("-topmost", 1)
        # refunds[refund_id].configure(background="#BEBEBE")


        L1 = Label(refunds[refund_id], text="IGN")
        L1.grid(row=0, column=0, sticky="e")

        E1 = Entry(refunds[refund_id], bd=3, width=27)
        E1.grid(row=0, column=1, sticky="e")


        L2 = Label(refunds[refund_id], text="SteamID (any)")
        L2.grid(row=1, column=0, sticky="e")

        E2 = Entry(refunds[refund_id], bd=3, width=27)
        E2.grid(row=1, column=1, sticky="e")


        L3 = Label(refunds[refund_id], text="Reason")
        L3.grid(row=2, column=0, sticky="e")

        # E3 = Entry(refunds[refund_id], bd=3)
        E3 = Text(refunds[refund_id], height=3, width=20, bd=3)
        E3.grid(row=2, column=1, sticky="e")


        L4 = Label(refunds[refund_id], text="Items Lost")
        L4.grid(row=3, column=0, sticky="e")

        # E4 = Entry(refunds[refund_id], bd=3)
        E4 = Text(refunds[refund_id], height=3, width=20, bd=3)
        E4.grid(row=3, column=1, sticky="e")


        L5 = Label(refunds[refund_id], text="Proof")
        L5.grid(row=4, column=0, sticky="e")

        E5 = Entry(refunds[refund_id], bd=3, width=27)
        E5.grid(row=4, column=1, sticky="e")

        if open_data != None:
            print("calling Data")
            E1.insert(0, refund_data[refund_id].get("IGN"))
            E2.insert(0, refund_data[refund_id].get("SteamID64"))
            E3.insert(END, refund_data[refund_id].get("Items Lost"))
            E4.insert(END, refund_data[refund_id].get("Reason"))
            E5.insert(0, refund_data[refund_id].get("Proof"))


        # L6 = Label(refunds[refund_id], text="Extra")
        # L6.grid(row=5, column=0, sticky="e")

        refund_data[refund_id] = {"IGN": E1.get(),
                                        "SteamID64": steam_64(str(E2.get())),
                                        "Items Lost": (E4.get(0.0, END)).strip(),
                                        "Reason": (E3.get(0.0, END)).strip(),
                                        "Proof": E5.get()}

        def copy_to_cb():
            pyperclip.copy(f"""IGN: {E1.get()}
SteamID64: {steam_64(str(E2.get()))}
Items Lost: {(E4.get(0.0, END)).strip()}
Reason: {(E3.get(0.0, END)).strip()}
Proof: {E5.get()}
""")
            refund_data[refund_id] = {"IGN": E1.get(),
                                        "SteamID64": steam_64(str(E2.get())),
                                        "Items Lost": (E4.get(0.0, END)).strip(),
                                        "Reason": (E3.get(0.0, END)).strip(),
                                        "Proof": E5.get()}
            # refunds[refund_id].destroy()
            save_data(refund_id=refund_id)

        def on_closing():
            refund_data[refund_id] = {"IGN": E1.get(),
                                        "SteamID64": steam_64(str(E2.get())),
                                        "Items Lost": (E4.get(0.0, END)).strip(),
                                        "Reason": (E3.get(0.0, END)).strip(),
                                        "Proof": E5.get()}
            save_data(refund_id=refund_id)
            refunds[refund_id].destroy()
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     root.destroy()

        refunds[refund_id].protocol("WM_DELETE_WINDOW", on_closing)
        save_data(refund_id=refund_id)


        B1 = Button(refunds[refund_id], text="Copy to clipboard", command=copy_to_cb)
        B1.grid(row=7, column=0, sticky="e")

        B1 = Button(refunds[refund_id], text="Copy Question", command=copy_question_to_cb)
        B1.grid(row=7, column=1, sticky="e")

        # refunds.update({refund_id: refunds[refund_id]})

        refunds[refund_id].mainloop()

    Lb1.grid(row=1, column=0, sticky="w")


    B2 = Button(topFrame, text="New Template", command=new_refund)
    B2.grid(row=0, column=2, sticky="w")

    def open_existing():
        index = Lb1.curselection()
        refund_id = Lb1.get(index)
        print(f"opening: {refund_id}")
        new_refund(open_data=refund_id)

    def delete_existing():
        index = Lb1.curselection()
        refund_id = Lb1.get(index)
        print(f"Deleting: {refund_id}")
        if messagebox.askokcancel("Delete", f"Are you sure you want to delete {refund_id}?"):
            delete_data(refund_id=refund_id)
            Lb1.delete(index)
            refund_data.pop(refund_id)

    def rename_existing():
        index = Lb1.curselection()
        refund_id = Lb1.get(index)

        Entry_id = Toplevel()
        EIDL1 = Label(Entry_id, text="New Name").grid(row=0, column=0, sticky="e")
        EID1 = Entry(Entry_id)
        EID1.grid(row=0, column=1, sticky="w")
        EID1.insert(0, "refund-")

        def commit_change():
            new_refund_id = EID1.get()
            if messagebox.askokcancel("Delete", f"Are you sure you want to rename {refund_id} to {new_refund_id}?"):
                rename_data(old_refund_id=refund_id, new_refund_id=new_refund_id)
                Lb1.delete(index)
                Lb1.insert(1, new_refund_id)
                refund_data.update({new_refund_id: refund_data.pop(refund_id)})
                Entry_id.destroy()
            else:
                Entry_id.destroy()

        EIDB = Button(Entry_id, text="Rename", command=commit_change)
        EIDB.grid(row=1, column=1, sticky="w")
        Entry_id.mainloop()

    B3 = Button(middleLeftFrame, text="Open Template", command=open_existing)
    B3.grid(row=1, column=0, sticky="nw")

    B4 = Button(middleLeftFrame, text="Rename Template", command=rename_existing)
    B4.grid(row=2, column=0, sticky="nw")

    B5 = Button(middleLeftFrame, text="Close Template", command=delete_existing)
    B5.grid(row=3, column=0, sticky="nw")

    B6 = Button(middleLeftFrame, text="Copy Question", command=copy_question_to_cb, bg="yellow")
    B6.grid(row=4, column=0, sticky="nw")

    if frame == None:
        Main.mainloop()


def Staff_apps_app(frame=None):
    if frame == None:
        Main = Tk()
        Main.title("Staff Application Response Maker")
    else:
        Main = frame

    EntryLength=27

    FrameLeft = Frame(Main)
    FrameLeft.grid(row=0, column=0)

    FrameRight = Frame(Main)
    FrameRight.grid(row=0, column=1)

    L1 = Label(FrameLeft, text="+ Rep")
    L1.grid(row=0, column=0, sticky="e")

    E1 = Entry(FrameLeft, bd=3, width=EntryLength)
    E1.grid(row=0, column=1, sticky="e")


    L2 = Label(FrameLeft, text="+/- Rep")
    L2.grid(row=1, column=0, sticky="e")

    E2 = Entry(FrameLeft, bd=3, width=EntryLength)
    E2.grid(row=1, column=1, sticky="e")


    L3 = Label(FrameLeft, text="- Rep")
    L3.grid(row=2, column=0, sticky="e")

    # E3 = Text(Main, height=3, width=20, bd=3)
    E3 = Entry(FrameLeft, bd=3, width=EntryLength)
    E3.grid(row=2, column=1, sticky="e")


    L4 = Label(FrameLeft, text="Comment")
    L4.grid(row=3, column=0, sticky="e")

    # E4 = Entry(Main, bd=3)
    E4 = Text(FrameLeft, height=5, width=20, bd=3)
    E4.grid(row=3, column=1, sticky="e")


    L4 = Label(FrameRight, text="Rating")
    L4.grid(row=0, column=0, sticky="e")

    var = DoubleVar()
    scale = Scale(FrameRight, variable=var, from_=0, to=5, resolution=0.1)
    scale.grid(row=1, column=0)



    if frame == None:
        Main.mainloop()



def main_app(frame=None):
    if frame == None:
        Main = Tk()
        Main.title("Elitelupus Refund Template Maker")
    else:
        Main = frame

    tabControl = ttk.Notebook(Main)

    refund_tab = ttk.Frame(tabControl)
    tabControl.add(refund_tab, text="Refunds")
    refund_page_tab = refund_app(refund_tab)


    refund_tab = ttk.Frame(tabControl)
    tabControl.add(refund_tab, text="Ban Extentions")


    staff_apps_tab = ttk.Frame(tabControl)
    tabControl.add(staff_apps_tab, text="Staff Applications")
    staff_apps_page_tab = Staff_apps_app(staff_apps_tab)


    refund_tab = ttk.Frame(tabControl)
    tabControl.add(refund_tab, text="LOA Requests")

    # cal = Calendar(refund_tab, selectmode = 'day',
    #                year = 2021, month = 5,
    #                day = 22)

    # cal.pack(pady = 20)

    # def grad_date():
    #     date.config(text = "Selected Date is: " + cal.get_date())

    # # Add Button and Label
    # Button(refund_tab, text = "Get Date",
    #        command = grad_date).pack(pady = 20)

    # date = Label(refund_tab, text = "")
    # date.pack(pady = 20)


    tabControl.pack(fill="both")

    if frame == None:
        Main.mainloop()


if __name__ == '__main__':
    main_app()

