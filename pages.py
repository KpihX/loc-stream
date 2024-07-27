#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk

from tkinter import simpledialog

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
        self.app.show_page("Meet")
        
        self.app.meeting = Meeting()
        self.app.meeting.start_meet()
        
    def join_meet(self)-> None:
        meeting_code = simpledialog.askstring("Meeting Code", "Enter the meeting code: ")
        self.app.pages["Meet"] = MeetPage(self.app)
        self.app.show_page("Meet")
        
        self.app.meeting = Meeting()
        self.app.meeting.join_meet(meeting_code)
        
class MeetPage(tk.Frame):
    def __init__(self, app:'App')-> None:
        super().__init__(master=app.main_frame)
        self.app = app
        self.create_widgets()
        
    def create_widgets(self)-> None:
        self.leave_meet_btn = tk.Button(self, text="Leave Meet", command=self.leave_meet)
        self.leave_meet_btn.pack(side=tk.RIGHT)
        
        self.participants_label = tk.Label(self, text="Participants: ")
        self.participants_label.pack(pady=10, side=tk.RIGHT)
        
        self.participants_list = tk.Listbox(self)
        self.participants_list.pack(pady=10, side=tk.RIGHT)
        
        self.screen_stream_btn = tk.Button(self, text="Share Screen", command=self.screen_stream)
        self.screen_stream_btn.pack(pady=10, side=tk.BOTTOM)
        
        self.file_stream_btn = tk.Button(self, text="Share File", command=self.file_stream)
        self.file_stream_btn.pack(pady=10, side=tk.BOTTOM)
        
    def screen_stream(self)-> None:
        pass
    
    def file_stream(self)-> None:
        pass
    
    def leave_meet(self)-> None:
        self.app.show_page("Home")
    
if __name__ == '__main__':
    import pages
    print(help(pages))
    input("Glad to have served you! Press 'Enter' to quit.")