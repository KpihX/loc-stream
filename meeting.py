#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import socket
import threading
import pickle
import tkinter as tk

from dotenv import load_dotenv
from tkinter import messagebox

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages import MeetPage

load_dotenv()

PORT = int(os.getenv("PORT"))
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS"))
INFO_MAX_LEN = 1024
MAX_CHUNK_SIZE = 4096
ACCEPT_SIGNAL = "1"
REFUSED_SIGNAL = "-1"

class Meeting:
    def __init__(self, page:'MeetPage')-> None:
        self.page:MeetPage = page
        self.ip = self.page.ip
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen_sharing_client = None
        
    def generate_meet_code(self):
        return self.ip
    
    def inv_gen_meet_code(self):
        return self.meet_code
    
    def start_meet(self)-> None:
        self.port = PORT
        self.meet_code = self.generate_meet_code()
        self.socket.bind((self.ip, self.port))
        self.page.participants_sockets[self.ip] = self.socket
        self.socket.listen(MAX_CONNECTIONS)
        print(f"Meeting started with code: {self.meet_code}")
    
        threading.Thread(target=self.accept_connections).start()
    
    def accept_connections(self):
        while True:
            client_socket, client_addr = self.socket.accept()
            print(f"Connection from {client_addr}")
            client_ip = client_addr[0]
            threading.Thread(target=self.handle_client, args=(client_socket, client_ip)).start()
            
    def handle_client(self, client_socket:socket.socket, client_ip)-> None:
        client_infos = client_socket.recv(INFO_MAX_LEN)
        client_login = pickle.loads(client_infos)
        print(f"Client login: {client_login}")
        
        if messagebox.askyesno("Accept participant", f"Do you want to accept the participant of login '{client_login}' at the ip address '{client_ip}' ?"):
            client_socket.sendall(ACCEPT_SIGNAL.encode())
            client_socket.sendall(pickle.dumps(self.page.participants))
            self.page.participants[client_ip] = {
                "login": client_login,
            }
            self.page.participants_sockets[client_ip]
            self.page.participants_frames[client_ip] = self.page.ParticipantFrame(self.page.participants_frame, client_ip, self.page.participants[client_ip])
            self.page.participants_frames[client_ip].pack()
        else:
            client_socket.sendall(REFUSED_SIGNAL.encode())
            client_socket.close()
    
    def join_meet(self, meet_code:str)-> None:     
        self.meet_code = meet_code
        print(f"Server address = ({self.inv_gen_meet_code()}, {PORT})")
        try:
            self.socket.connect((self.inv_gen_meet_code(), PORT))
        except socket.gaierror:
            messagebox.showerror("Error", "Invalid meet code!")
            return
        except OSError:
            messagebox.showwarning("Warning", "You provided a wrong meet code")
            return
            
        infos = self.page.app.login.get()
        self.socket.sendall(pickle.dumps(infos))
        
        messagebox.showinfo("Success", "Wait for the meet organiser to let you enter!")
        
        if self.socket.recv(INFO_MAX_LEN).decode() == REFUSED_SIGNAL:
            messagebox.showwarning("Warning", "The meet organizer didn't accept your invitation to join the meet!")
            return
        
        messagebox.showinfo("Success", "Welcome to the meet!")
        
        
        self.page.app.pages["Meet"].pack(fill=tk.BOTH, expand=True)
        self.page.app.show_page("Meet")
        
        current_participants:dict[str, dict[str, any]] = pickle.loads(self.socket.recv(MAX_CHUNK_SIZE))
        print(f"Current participants: {current_participants}")
        self.page.participants.update(current_participants)
        for participant_ip, participant in current_participants.items():
            self.page.participants_frames[participant_ip] = self.page.ParticipantFrame(self.page.participants_frame, participant_ip, participant)
            self.page.participants_frames[participant_ip].pack()

if __name__ == '__main__':
    
    input("Glad to have served you! Press 'Enter' to quit.")