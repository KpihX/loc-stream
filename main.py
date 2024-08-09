import tkinter as tk
from tkinter import ttk
import socket
import threading

import tkinter as tk
from tkinter import ttk, Frame, Label, Button, Entry, END, BOTH, DISABLED, NORMAL


def printHello():
    print('hello world')


class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.configure(bg='#678BAF')

        # configuration de l'entête
        self.header = Frame(self, background='', height=100)
        self.header.pack(side="top", fill="x")

        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=1)

        self.leftHeader = Frame(self.header, background='green', height=100)
        self.leftHeader.grid(row=0, column=0, sticky="w")

        self.centerHeader = Frame(self.header, background='green', height=100)
        self.centerHeader.grid(row=0, column=1, sticky="")

        self.rightHeader = Frame(self.header, background='green', height=100)
        self.rightHeader.grid(row=0, column=2, sticky="e")

        self.logo = Label(self.leftHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo.grid(row=0, column=0, sticky="w")
        self.logo10 = Label(self.centerHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo10.grid(row=0, column=0, sticky="")
        self.logo2 = Label(self.rightHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo2.grid(row=0, column=2, sticky="e")

        # création du body
        self.body = Frame(self, bg='#678BAF')
        self.body.pack(side="top", fill="both", expand=True)

        self.body1 = Frame(self.body, background='white', height=120)
        self.body1.pack(side='top', fill=BOTH, expand=0)

        self.body2 = Frame(self.body, background='white')
        self.body2.pack(side='bottom', fill=BOTH, expand=1)

        self.textTitle = Label(self.body1, text='welcome to KAM-MEET', font=('Arial', 40, 'bold italic'), bg='white',
                               pady=150)
        self.textTitle.pack()

        self.body2.grid_columnconfigure(0, weight=1)
        self.body2.grid_columnconfigure(1, weight=1)
        self.body2.grid_columnconfigure(2, weight=1)

        self.leftBody2 = Frame(self.body2, background='green', height=100)
        self.leftBody2.grid(row=0, column=0, sticky="w")

        self.centerBody2 = Frame(self.body2, background='white', height=100)
        self.centerBody2.grid(row=0, column=1, sticky="")

        self.rightBody2 = Frame(self.body2, background='green', height=100)
        self.rightBody2.grid(row=0, column=2, sticky="e")

        # contenu
        self.startMeetButton = Button(self.centerBody2, text='lancer un meet', font=('Arial', 20, 'bold'),
                                      command=lambda: self.controller.show_frame("MeetPage"), pady=10, padx=10)
        self.startMeetButton.grid(column=0, row=0, padx=20)

        self.placeholder_text = 'Veuillez entrer le code du meet'
        self.joinMeetInput = Entry(self.centerBody2, font=('Arial', 20), fg='grey')
        self.joinMeetInput.insert(0, self.placeholder_text)
        self.joinMeetInput.grid(row=0, column=1, padx=10)

        self.joinMeetInput.bind("<FocusIn>", self.on_entry_click)
        self.joinMeetInput.bind("<FocusOut>", self.on_focus_out)
        self.joinMeetInput.bind("<KeyRelease>", self.check_entry_text)

        self.joinMeetButton = Button(self.centerBody2, text='rejoindre un meet', font=('Arial', 20, 'bold'),
                                     state=DISABLED, command=lambda: self.on_button_click(), pady=10, padx=10)
        self.joinMeetButton.grid(column=2, row=0, padx=5)

        self.shareFile = Button(self.centerBody2, text='Share File', font=('Arial', 20, 'bold'),
                                command=lambda: printHello(), pady=10, padx=10)
        self.shareFile.grid(column=1, row=3, padx=20)

    @staticmethod
    def _create_server_socket():
        host = '127.0.0.1'  # Localhost
        port = 65432  # Port to listen on (non-privileged ports are > 1023)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f'Server started at {host}:{port}')
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def on_entry_click(self, event):
        if self.joinMeetInput.get() == self.placeholder_text:
            self.joinMeetInput.delete(0, END)
            self.joinMeetInput.config(fg='black')

    def on_focus_out(self, event):
        if self.joinMeetInput.get() == '':
            self.joinMeetInput.insert(0, self.placeholder_text)
            self.joinMeetInput.config(fg='grey')

    def check_entry_text(self, event):
        if self.joinMeetInput.get() and self.joinMeetInput.get() != self.placeholder_text:
            self.joinMeetButton.config(state=NORMAL)
        else:
            self.joinMeetButton.config(state=DISABLED)

    def on_button_click(self):
        entered_text = self.joinMeetInput.get()
        if entered_text != self.placeholder_text:
            print(f"Vous avez entré : {entered_text}")


class MeetPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#678BAF')

        self.header = Frame(self, background='green', height=100)
        self.header.pack(side="top", fill="x")

        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=1)

        self.body = Frame(self, bg='#678BAF')
        self.body.pack(side="top", fill="both", expand=True)

        self.footer = Frame(self, bg='green', height=50)
        self.footer.pack(side="bottom", fill="x")

        self.screenShare = Frame(self.body, bg='white')
        self.participant = Frame(self.body, background='black', width=300)
        self.participant.pack(side="right", fill="both")
        self.screenShare.pack(side="left", fill="both", expand=True)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('KAM-MEET')

        # Obtenez les dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Calculer 80% des dimensions de l'écran
        default_width = int(0.8 * screen_width)
        default_height = int(0.8 * screen_height)
        # Calculer les coordonnées pour centrer la fenêtre
        x_position = (screen_width - default_width) // 2
        y_position = (screen_height - default_height) // 2
        # Définir une dimension par défaut de 80% de l'écran et centrer la fenêtre
        self.geometry(f"{default_width}x{default_height}+{x_position}+{y_position}")
        # taille minimale
        self.minsize(1200, 800)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, MeetPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
