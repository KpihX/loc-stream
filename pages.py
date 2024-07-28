#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk

from tkinter import simpledialog, Frame, messagebox
from PIL import Image, ImageTk

from meeting import Meeting

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import App

class HomePage(tk.Frame):
    def __init__(self, app:'App')-> None:
        self.app = app
        super().__init__(self.app.main_frame)
        self.create_widgets()
    
    def create_widgets(self):
        self.start_meet_btn = tk.Button(self, text="Start Meeting", command=self.start_meet)
        self.start_meet_btn.pack(pady=10)

        self.join_meet_btn = tk.Button(self, text="Join Meeting", command=self.join_meet)
        self.join_meet_btn.pack(pady=10)
        
    def start_meet(self)-> None:
        self.app.pages["Meet"] = MeetPage(self.app)
        self.app.pages["Meet"].pack(fill=tk.BOTH, expand=True)
        self.app.show_page("Meet")
        
        self.app.meeting = Meeting(self.app.pages["Meet"])
        self.app.meeting.start_meet()
        
    def join_meet(self)-> None:
        while True:
            meet_code = simpledialog.askstring("Meeting Code", "Enter the meeting code: ")
            if meet_code is None:
                return
            if meet_code == "":
                messagebox.showerror("Error", "You didn't enter a code")
                continue
            break
        
        self.app.pages["Meet"] = MeetPage(self.app)
        
        self.app.meeting = Meeting(self.app.pages["Meet"])
        self.app.meeting.join_meet(meet_code)
        
class MeetPage(tk.Frame):
    def __init__(self, app:'App')-> None:
        super().__init__(master=app.main_frame)
        self.app = app
        self.ip = self.app.ip
        self.participants = {self.ip:{"login": f"{self.app.login.get()}"}}
        self.participants_frames = {}
        self.participants_sockets = {}
        
        self.create_widgets()
        
    class ParticipantFrame(tk.Frame):
        def __init__(self, master, participant_ip, participant:dict[str, str]):
            super().__init__(master=master)
            self.configure(bg="#f0f0f0")
            
            self.login_label = tk.Label(self, text=participant["login"])
            self.login_label.pack(padx=3, pady=3)
            
            self.ip_label = tk.Label(self, text=participant_ip)
            self.ip_label.pack(padx=3, pady=3)
            
        
    def create_widgets(self)-> None:    
        self.main_frame = Frame(self)
        self.main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.bind("<Configure>", self.resize_bg)
        
        self.bg_image = Image.open("bgs/bg.jpeg")
        self.bg = None
        
        self.func_btns_frame = Frame(self.main_frame)
        self.func_btns_frame.pack(side=tk.BOTTOM)
            
        self.screen_stream_btn = tk.Button(self.func_btns_frame, text="Share Screen", command=self.screen_stream)
        self.screen_stream_btn.pack(padx=10, pady=10, side=tk.LEFT)
        
        self.leave_meet_btn = tk.Button(self.func_btns_frame, text="Leave Meet", command=self.leave_meet)
        self.leave_meet_btn.pack(padx=10, pady=10, side=tk.RIGHT)
        
        self.file_stream_btn = tk.Button(self.func_btns_frame, text="Share File", command=self.file_stream)
        self.file_stream_btn.pack(padx=10, pady=10, side=tk.RIGHT)
        
        
        self.participants_frame = Frame(self)
        self.participants_frame.pack(side=tk.RIGHT)
        
        self.participants_label = tk.Label(self.participants_frame, text="Participants")
        self.participants_label.pack(pady=10)
        
        self.participants_frames[self.ip] = self.ParticipantFrame(self.participants_frame, self.ip, self.participants[self.ip])
        self.participants_frames[self.ip].pack()
        
        
    def resize_bg(self, event):
        canvas_width = event.width
        canvas_height = event.height
        print("Meet canvas dim:", (canvas_width, canvas_height))
        
        resized_image = self.bg_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg)
        
    def screen_stream(self)-> None:
        pass
    
    def file_stream(self)-> None:
        pass
    
    def leave_meet(self)-> None:
        self.app.show_page("Home")
    
if __name__ == '__main__':
    import pages
    print(help(pages))
    input("\nGlad to have served you! Press 'Enter' to quit.")