#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk

import database.users_controller as du

from tkinter import Frame, messagebox, Tk

from components import Header, Footer, Register
from pages import HomePage

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from meeting import Meeting

class App(tk.Frame):
    def __init__(self, master:Tk)-> None:
        super().__init__(master)
        self.master = master
        self.meeting: Meeting
        self.login = tk.StringVar()
        self.close = False
        
        du.create_users()
        users = du.get_users()
        print(f"users = {users}")
        if len(users) == 0:
            self.register_popup = Register(self, self.handle_register)
        else:
            self.login.set(users[0][0])
        if self.close:
            self.quit()
            exit(1)
        else:
            self.create_widgets()

    def create_widgets(self)-> None:
        self.header = Header(self)
        self.header.pack(fill=tk.X)
        
        self.footer = Footer(self)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.main_frame = tk.Frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        print("Header & Footer displayed.")
        
        self.pages:Dict[str, Frame] = {}
        self.pages["Home"] = HomePage(self)
        self.show_page("Home")
    
    def handle_register(self, login):
        messagebox.showinfo("Success", f"You are connected as '{login}'")
        self.login.set(login)
        du.add_user(login)
        
    def handle_login_change(self, login):
        du.update_user(self.login.get(), login)
        self.login.set(login)
        messagebox.showinfo("Success", f"You new login is '{login}'")
        
    def show_page(self, page_name):
        try:
            self.current_page.pack_forget()
        except AttributeError:
            pass
            
        self.current_page = self.pages[page_name]
        self.current_page.pack()
        # self.current_page.tkraise()
       
if __name__ == '__main__':
    import ui
    print(help(ui))
    input("Glad to have served you! Press 'Enter' to quit.")