from tkinter import *
from pygame import *

from interface.Landing import *


def printHello():
    print('hello world')


def initialize_ui(app):
    # Obtenez les dimensions de l'écran
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculer 80% des dimensions de l'écran
    default_width = int(0.8 * screen_width)
    default_height = int(0.8 * screen_height)

    # Calculer les coordonnées pour centrer la fenêtre
    x_position = (screen_width - default_width) // 2
    y_position = (screen_height - default_height) // 2

    # Définir une dimension par défaut de 80% de l'écran et centrer la fenêtre
    app.geometry(f"{default_width}x{default_height}+{x_position}+{y_position}")


class MyApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configuration de la fenêtre principale
        self.title('KAM-MEET')

        # creation du header
        self.header = Frame(self, background='', height=100)
        self.header.pack(side="top", fill="x")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=1)

        # division du header en 3
        self.leftHeader = Frame(self.header, background='green', height=100)
        self.leftHeader.grid(row=0, column=0, sticky="w")

        self.centerHeader = Frame(self.header, background='green', height=100)
        self.centerHeader.grid(row=0, column=1, sticky="")

        self.rightHeader = Frame(self.header, background='green', height=100)
        self.rightHeader.grid(row=0, column=2, sticky="e")

        # creation du body
        self.body = Frame(self, bg='#678BAF')  # Enlever la composante alpha
        self.body.pack(side="top", fill="both", expand=True)

        # creation du footer
        self.footer = Frame(self, bg='green', height=50)
        self.footer.pack(side="bottom", fill="x")
        initialize_ui(self)


class Meet(MyApp):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.screenShare = Frame(self.body, bg='white')
        self.participant = Frame(self.body, background='black', width=300)
        self.participant.pack(side="right", fill="both")
        self.screenShare.pack(side="left", fill="both", expand=True)


if __name__ == "__main__":
    app = Meet()
    app.mainloop()
