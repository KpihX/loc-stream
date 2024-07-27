import tkinter as tk
import os
import threading
import socket

from dotenv import load_dotenv
from tkinter import filedialog, messagebox

load_dotenv()

send_path_dotenv = os.path.join(os.path.dirname(__file__), ".env.send")
load_dotenv(dotenv_path=send_path_dotenv)

RECV_ADDRESS=os.getenv("RECV_ADDRESS")
RECV_PORT=int(os.getenv("RECV_PORT"))

MAX_CHUNK_SIZE=int(os.getenv("MAX_CHUNK_SIZE"))
ACCEPT_SIGNAL=os.getenv("ACCEPT_SIGNAL")

class FileSendFrame(tk.Frame):
    def __init__(self, master:tk.Tk)-> None:
        super().__init__(master)
        self.master = master
        
        self.file_ind_label = tk.Label(self, text="")
        self.file_ind_label.pack()
        
        self.file_label = tk.Label(self, text="No file selected!")
        self.file_label.pack()
        
        self.file_select_btn = tk.Button(self, text="Select a file", command=self.select_file)
        self.file_select_btn.pack()
        
        self.send_btn = tk.Button(self, text="Send the file", comman=self.send_file, state=tk.DISABLED)
        self.send_btn.pack()
        
        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack()
        
    def select_file(self)-> None:
        file_path = filedialog.askopenfilename()
        self.progress_label.config(text="")
        if file_path:
            self.file_label.config(text=f"{file_path}")
            self.file_ind_label.config(text="Selected file: ")
            self.file_select_btn.config(text="Select another file")
            self.send_btn.config(state=tk.NORMAL)
            
    def send_file(self, recv_address=RECV_ADDRESS, recv_port=RECV_PORT)-> None:
        file_path = self.file_label.cget("text")
        if not file_path:       
            return
        print("File_path:", file_path)
        threading.Thread(target=self.send_file_thread, args=(file_path, recv_address, recv_port)).start()
        
    def send_file_thread(self, file_path, recv_address, recv_port, accept_signal=ACCEPT_SIGNAL):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Sender socket created!")
                print(f"Trying to connect to the recv: ({recv_address}, {recv_port})")
                s.connect((recv_address, recv_port))
                print(f"Sender connected to the receiver: ({recv_address}, {recv_port})")
                s.sendall(os.path.basename(file_path).encode())
                response = s.recv(1).decode()
                print(f"Recv response: {response}")
                
                if response == accept_signal:
                    with open(file_path, "rb") as f:
                        total_size = os.path.getsize(file_path)
                        sent_size = 0
                        while chunk := f.read(MAX_CHUNK_SIZE):
                            s.sendall(chunk)
                            sent_size += len(chunk)
                            progress = (sent_size / total_size) * 100 if total_size > 0 else 100
                            self.progress_label.config(text=f"Progression: {progress:.2f}")
                    messagebox.showinfo("Succes", "The file has been successfully sent!")
                else:
                    messagebox.showinfo("Refusal", "The receiver refused the file!")
        except Exception as e:
            raise
        
        
class FileSendApp(tk.Frame):
    def __init__(self, master:tk.Tk)-> None:
        super().__init__(master)
        self.file_send_frame = FileSendFrame(self)
        self.file_send_frame.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = FileSendApp(root)
    app.pack()
    root.title("File Sending")
    root.mainloop()
    
    input("\nGlad to have served you! Press 'Enter' to quit.")