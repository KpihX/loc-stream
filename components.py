#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk

from PIL import Image, ImageTk
from typing import TYPE_CHECKING
from tkinter import messagebox

if TYPE_CHECKING:
    from ui import App

class Header(tk.Frame):
    def __init__(self, master:"App")-> None:
        super().__init__(master)
        self.master:App = master
        self.BG_COLOR = '#FFA07A'
        self.config(pady=1, bg=self.BG_COLOR)
        
        self.title_frame = tk.Frame(self, bg=self.BG_COLOR)
        self.title_frame.pack(side=tk.LEFT, padx=7)
    
        self.LOGO_HEIGHT = 40
        self.LOGO_WIDTH = 40
    
        self.logo_canvas = tk.Canvas(self.title_frame, width=self.LOGO_WIDTH, height=self.LOGO_HEIGHT, bg=self.BG_COLOR)
        self.logo_canvas.pack(padx=7, side=tk.LEFT)
        logo = Image.open("logos/logo.png").resize((self.LOGO_WIDTH, self.LOGO_HEIGHT))
        self.logo = ImageTk.PhotoImage(logo)
        self.logo_canvas.create_image(0, 0, anchor=tk.NW, image=self.logo)
        
        self.label = tk.Label(self.title_frame, text="K&K Meet", bg=self.BG_COLOR)
        self.label.pack(side=tk.RIGHT, padx=7)
        
        self.account_btn = tk.Button(self, textvariable=self.master.login, bg=self.BG_COLOR)
        self.account_btn.pack(side=tk.RIGHT, padx=7)
        self.account_btn.bind("<Button-1>", self.show_dropdown)
        
        self.dropdown_menu = tk.Menu(master, tearoff=0)
        self.dropdown_menu.add_command(label="Change login", command=self.handle_change_login)
                                
    def show_dropdown(self, event)-> None:
        self.dropdown_menu.post(event.x_root, event.y_root)

    
    def handle_change_login(self):
        self.login_settings = LoginSettings(self.master, self.master.handle_login_change)           

class LoginSettings(tk.Toplevel):
    def __init__(self, master:"App", login_callback)-> None:
        super().__init__(master)
        self.master:App = master
        self.title("Login settings")
        self.login_callback = login_callback
        
        self.login_label = tk.Label(self, text="Login")
        self.login_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.login_var = tk.StringVar()
        print(f"Old login: {self.master.login.get()}")
        self.login_var.set(self.master.login.get())
        self.login_entry = tk.Entry(self, textvariable=self.login_var)
        self.login_entry.grid(row=0, column=1, padx=20, pady=10)
        
        self.validate_btn = tk.Button(self, text="Save", command=self.submit)
        self.validate_btn.grid(row=1, column=0, pady=10, columnspan=2)
        
        self.transient(self.master) # Ensure that the popup is in front of the main frame (master)
        self.grab_set() # To have a modal popup
        
        # self.geometry("300x100") 
        # self.update_idletasks()
        
        # self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.wait_window(self) # Wait for self to be closed
        
    def submit(self)-> None:
        login = self.login_entry.get()
        if not login:
            messagebox.showerror("Error", "No login provided!")
            return
        print(f"New login: {login}")
        self.login_callback(login)
        self.destroy()
        
    # def on_close(self)-> None:
    #     print("Closing of the login settings popup")
        

class Footer(tk.Frame):
    def __init__(self, master)-> None:
        super().__init__(master)
        self.label = tk.Label(self, text="© 2024 K&K Meet App. By K𝛑X & Shadow", bg="blue", fg="white")
        self.label.pack()
        
class Register(tk.Toplevel):
    def __init__(self, master:"App", login_callback)-> None:
        super().__init__(master)
        self.master:App = master
        self.title("Let's start!")
        self.login_callback = login_callback
        # self.overrideredirect(True) # TO delete the title bar
        
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=7)
        
        self.login_label = tk.Label(self.login_frame, text="Login")
        self.login_label.pack(side=tk.LEFT, padx=7)
        
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.pack(side=tk.RIGHT, padx=7)
        
        self.validate_btn = tk.Button(self, text="Save", command=self.on_login)
        self.validate_btn.pack(pady=10)
        
        self.transient(self.master) # Ensure that the popup is in front of the main frame (master)
        self.grab_set() # To have a modal popup
        
        self.geometry("300x100") 
        self.update_idletasks()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.wait_window(self) # Wait for self to be closed
        
    def on_login(self)-> None:
        login = self.login_entry.get()
        if not login:
            messagebox.showerror("Error", "No login provided!")
            return
        print(f"Login: {login}")
        self.login_callback(login)
        self.destroy()
        
    def on_close(self)-> None:
        print("Closing of the register popup")
        messagebox.showwarning("Good bye!", "You must have a login to be identify friendly while being in a meet!")
        self.master.close = True
        self.destroy()

if __name__ == '__main__':
    import components
    print(help(components))
    input("Glad to have served you! Press 'Enter' to quit.")