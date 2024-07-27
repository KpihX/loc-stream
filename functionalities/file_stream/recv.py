#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import tkinter as tk
import threading
import socket
import os

from dotenv import load_dotenv
from tkinter import filedialog, messagebox

load_dotenv()
recv_dotenv = os.path.join(os.path.dirname(__file__), ".env.recv")
load_dotenv(recv_dotenv)

RECV_ADDRESS = os.getenv("RECV_ADDRESS")
RECV_PORT = int(os.getenv("RECV_PORT"))
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE"))
ACCEPT_SIGNAL = os.getenv("ACCEPT_SIGNAL")
REFUSE_SIGNAL=os.getenv("REFUSE_SIGNAL")
MAX_SENDERS = int(os.getenv("MAX_SENDERS"))
MAX_FILENAME_SIZE = int(os.getenv("MAX_FILENAME_SIZE"))

class FileRecvFrame(tk.Frame):  
    def __init__(self, master:tk.Tk)-> None:
        super().__init__(master)
        self.master = master
        
        self.progress_label = tk.Label(self, text="Waiting for reception")
        self.progress_label.pack()
        
        print("We are trying to start the server")
        threading.Thread(target=self.start_server).start()    

    def start_server(self, recv_address=RECV_ADDRESS, recv_port=RECV_PORT, max_senders=MAX_SENDERS)-> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((recv_address, recv_port))
            s.listen(max_senders)
            while True:
                send_socket, _ = s.accept()
                threading.Thread(target=self.handle_sender, args=(send_socket,)).start()
                    
    def handle_sender(self, client_socket:socket.socket, accept_signal=ACCEPT_SIGNAL, max_chunk_size=MAX_CHUNK_SIZE, refuse_signal=REFUSE_SIGNAL, max_filename_size=MAX_FILENAME_SIZE)-> None:
        try:
            file_name = client_socket.recv(max_filename_size).decode()
            if not file_name:
                return
            
            if messagebox.askyesno("Receive file", f"Do you want to receive the file '{file_name}'"):
                client_socket.sendall(accept_signal.encode())
                save_path = filedialog.asksaveasfilename(initialfile=file_name)
                if save_path:
                    with open(save_path, "wb") as f:
                        total_size = 0
                        self.progress_label.config(text="While receptioning!")
                        while chunk := client_socket.recv(max_chunk_size):
                            f.write(chunk)
                            total_size += len(chunk)
                            # TODO: config progress 
                    self.progress_label.config(text="Waiting for another reception!")
                    messagebox.showinfo("Success", "File received with success!")
            else:
                client_socket.sendall(refuse_signal.encode())
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client_socket.close()

class FileRecvApp(tk.Frame):
    def __init__(self, master:tk.Tk)-> None:
        super().__init__(master)
        self.master = master
        self.file_recv_frame = FileRecvFrame(self)
        self.file_recv_frame.pack()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("File Reception")
    app = FileRecvApp(root)
    app.pack()
    root.mainloop()
    
    input("\nGlad to have served you! Press 'Enter' to quit.")