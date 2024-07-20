from tkinter import Frame

from interface.PageTemplate import *
from interface.PageTemplate import MyApp


class Home(MyApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HeaderManager()

        self.BodyManager()

    # gestion de l'entête du home
    def HeaderManager(self):
        self.logo = Label(self.leftHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo.grid(row=0, column=0, sticky="w")
        self.logo10 = Label(self.centerHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo10.grid(row=0, column=0, sticky="")
        self.logo11 = Label(self.centerHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo11.grid(row=0, column=1, sticky="")
        self.logo12 = Label(self.centerHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo12.grid(row=0, column=2, sticky="")
        self.logo13 = Label(self.centerHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo13.grid(row=0, column=3, sticky="")
        self.logo2 = Label(self.rightHeader, text='KAM_MEET', bg='green', pady=10, padx=5, font='Arial')
        self.logo2.grid(row=0, column=2, sticky="e")

    def BodyManager(self):
        # subdivision du body
        self.body1 = Frame(self.body, background='white', height=120)
        self.body1.pack(side='top', fill=BOTH, expand=0)

        self.body2 = Frame(self.body, background='white')
        self.body2.pack(side='bottom', fill=BOTH, expand=1)

        self.textTitle = Label(self.body1, text='welcome to KAM-MEET', font=('Arial', 40, 'bold italic'), bg='white', pady=150)
        self.textTitle.pack()

        # subdivision du body2
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
        self.startMeetButton = Button(self.centerBody2, text='lancer un meet', font=('Arial', 20, 'bold'), command=lambda: printHello(), pady=10, padx=10)
        self.startMeetButton.grid(column=0, row=0, padx=20)

        self.placeholder_text = 'Veuillez entrer le code du meet'
        self.joinMeetInput = Entry(self.centerBody2, font=('Arial', 20), fg='grey')
        self.joinMeetInput.insert(0, self.placeholder_text)
        self.joinMeetInput.grid(row=0, column=1, padx=10)

        self.joinMeetInput.bind("<FocusIn>", self.on_entry_click)
        self.joinMeetInput.bind("<FocusOut>", self.on_focus_out)
        self.joinMeetInput.bind("<KeyRelease>", self.check_entry_text)

        self.joinMeetButton= Button(self.centerBody2, text='rejoindre un meet', font=('Arial', 20, 'bold'), state=DISABLED, command=lambda: printHello(), pady=10, padx=10)
        self.joinMeetButton.grid(column=2, row=0, padx=5)

    def on_entry_click(self, event):
        """Fonction pour supprimer le placeholder lorsque l'utilisateur clique sur le champ de saisie."""
        if self.joinMeetInput.get() == self.placeholder_text:
            self.joinMeetInput.delete(0, END)
            self.joinMeetInput.config(fg='black')

    def on_focus_out(self, event):
        """Fonction pour remettre le placeholder si le champ de saisie est vide lorsque l'utilisateur perd le focus."""
        if self.joinMeetInput.get() == '':
            self.joinMeetInput.insert(0, self.placeholder_text)
            self.joinMeetInput.config(fg='grey')

    def check_entry_text(self, event):
        """Active le bouton si l'entrée n'est pas vide, sinon le désactive."""
        if self.joinMeetInput.get() and self.joinMeetInput.get() != self.placeholder_text:
            self.joinMeetButton.config(state=NORMAL)
        else:
            self.joinMeetButton.config(state=DISABLED)

    def on_button_click(self):
        entered_text = self.joinMeetInput.get()
        if entered_text != self.placeholder_text:
            print(f"Vous avez entré : {entered_text}")