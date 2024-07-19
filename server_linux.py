import socket
import threading
import subprocess
import io
from PIL import Image

def send_screenshot(client_socket):
    try:
        while True:
            # Utiliser ffmpeg avec une taille de buffer de probabilité augmentée
            ffmpeg_command = [
                'ffmpeg', '-f', 'x11grab', '-probesize', '50M', '-video_size', '1366x768', '-i', ':0.0', 
                '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'
            ]
            ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
            img_bytes, _ = ffmpeg_process.communicate()
            
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='JPEG')
            img_bytes = byte_arr.getvalue()
            size = len(img_bytes)
            
            if size > 1024 * 1024:  # Vérification si la taille de l'image dépasse 10 Mo
                print(f"Taille de l'image trop grande : {size} octets")
                continue
                
            print(f"Taille de l'image envoyée : {size} octets")
            
            client_socket.sendall(size.to_bytes(4, 'big'))
            
            for i in range(0, size, 4096):
                client_socket.sendall(img_bytes[i:i+4096])
    
            # Attendre le signal du client avant d'envoyer la prochaine image
            signal = client_socket.recv(1)
            if signal != b'1':
                print("Signal incorrect reçu, arrêt de l'envoi!")
                break
            
    except BrokenPipeError:
        print("Client déconnecté.")
        client_socket.close()
    except Exception as e:
        print(f"Erreur : {e}")
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))
    server_socket.listen(5)
    print("Serveur démarré.")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client connecté : {addr}")
        threading.Thread(target=send_screenshot, args=(client_socket,)).start()

if __name__ == '__main__':
    main()
