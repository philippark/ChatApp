import tkinter as tk
from tkinter import ttk
import socket
import random
from threading import Thread
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

NAME = ""

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Chat")
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Chat):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.frm = tk.Frame(master=self)
        
        #label
        self.lbl = tk.Label(master=self.frm, text="Name: ")
        self.lbl.grid(row=0, column=0)

        #text entry
        self.ent_name = ttk.Entry(master=self.frm, width = 20)
        self.ent_name.grid(row=1, column=0)

        #submit button
        self.btn_submit = ttk.Button(master=self.frm, text="Submit", command=lambda:[self.set_name(), controller.show_frame(Chat)])
        self.btn_submit.grid(row=1, column=1)

        self.frm.place(relx=.5, rely=.5, anchor="center")

    def set_name(self, *args):
        name_given = self.ent_name.get()

        global NAME

        if name_given != "":
            NAME = name_given
            self.ent_name.delete(0, tk.END)
    
            


class Chat(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        controller.bind("<Return>", self.send_message)

        self.name = "bob"

        """
        Chat frame and label
        """
        self.frm_chat = tk.Frame(master=self, relief=tk.SUNKEN, borderwidth=1)
        scroll = tk.Scrollbar(self, orient="vertical")
        scroll.grid(row=0, column=1, sticky="ns")

        self.txt_chat = tk.Text(master=self.frm_chat, width=40, height=20, state="disabled", yscrollcommand=scroll.set)
        scroll.config(command=self.txt_chat.yview)
        self.txt_chat.grid(row=0, column=0)

        """
        Message entry and send button 
        """
        self.frm_entry = tk.Frame(master=self)
        self.ent_entry = tk.Entry(master=self.frm_entry, width=40)
        self.btn_submit = ttk.Button(master=self.frm_entry, text="Send", command=self.send_message)

        self.ent_entry.grid(row=0, column=0, sticky="e")
        self.btn_submit.grid(row=0, column=1, sticky="w")

        """
        Formatting
        """
        self.frm_chat.grid(row=0, column=0)
        self.frm_entry.grid(row=1, column=0, padx=10)

        self.connect()

        t = Thread(target=self.listen_for_messages)
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()

    def send_message(self, *args):
        to_send = self.ent_entry.get()

        if (to_send == ""):
            return
        
        self.ent_entry.delete(0, tk.END)


        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"[{date_now}] {NAME}{separator_token}{to_send}"

        self.s.send(to_send.encode())

    
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.txt_chat.config(state="normal")
        self.txt_chat.insert('end', f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}..." + "\n")
        
        # connect to the server
        self.s.connect((SERVER_HOST, SERVER_PORT))
        self.txt_chat.insert('end', "[+] Connected." + "\n")

        self.txt_chat.config(state="disabled")

    def listen_for_messages(self):
        while True:
            message = self.s.recv(1024).decode()
            self.txt_chat.config(state="normal")
            self.txt_chat.insert('end', message + "\n")
            self.txt_chat.see("end")
            self.txt_chat.config(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()