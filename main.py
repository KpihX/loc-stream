#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk
from ui import App

if __name__ == '__main__':
    root =  tk.Tk()
    root.title("K&K Meet")
    root.geometry("800x600")
    
    app = App(root)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
    
    input("Glad to have served you! Press 'Enter' to quit.")