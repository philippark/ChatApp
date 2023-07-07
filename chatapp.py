import tkinter as tk
import socket
import random
from threading import Thread
from datetime import datetime

MESSAGE_GLOBAL = ""

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chat")
        self.resizable(width=False, height=False)
        self.bind("<Return>", self.send_message)

        """
        Chat frame and label
        """
        self.frm_chat = tk.Frame(master=self, relief=tk.SUNKEN, borderwidth=1)
        self.lbl_chat = tk.Label(master=self.frm_chat, width=40, height=20, text="Welcome to the chat room", anchor="nw", justify="left")
        self.lbl_chat.grid(row=0, column=0)

        """
        Message entry and send button 
        """
        self.frm_entry = tk.Frame(master=self)
        self.ent_entry = tk.Entry(master=self.frm_entry, width=40)
        self.btn_submit = tk.Button(master=self.frm_entry, text="Send", command=self.send_message)

        self.ent_entry.grid(row=0, column=0, sticky="e")
        self.btn_submit.grid(row=0, column=1, sticky="w")

        """
        Formatting
        """
        self.frm_chat.grid(row=0, column=0)
        self.frm_entry.grid(row=1, column=0, padx=10)


    def send_message(self, *args):
        message = self.ent_entry.get()

        if (message == ""):
            return
        
        self.lbl_chat["text"] += "\n" + message
        self.ent_entry.delete(0, tk.END)

    def print_message(self, message):
        if (message == ""):
            return
        
        self.lbl_chat["text"] += "\n" + message

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)
        MESSAGE_GLOBAL = message



if __name__ == "__main__":

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5002 # server's port
    separator_token = "<SEP>" # we will use this to separate the client name & message

    # initialize TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")


    # prompt the client for a name
    name = input("Enter your name: ")

    # make a thread that listens for messages to this client & print them
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:
        # input message we want to send to the server
        to_send =  input()
        # a way to exit the program
        if to_send.lower() == 'q':
            break
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"[{date_now}] {name}{separator_token}{to_send}"
        # finally, send the message
        s.send(to_send.encode())

        app = App()
        app.print_message(MESSAGE_GLOBAL)
        app.mainloop()

    # close the socket
    s.close()




