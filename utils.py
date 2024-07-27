import socket

def get_ip_address():
    # Create a socket object using IPv4 and UDP protocols
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # We don't actually connect to the server; this is just to get the local IP address
        # 8.8.8.8 is a public DNS server provided by Google
        # 80 is the port number for HTTP
        s.connect(("8.8.8.8", 80))
        
        # Get the local IP address of the socket
        ip_address = s.getsockname()[0]
    except OSError:
        # If there is an OSError Exception, default to the loopback address
        ip_address = "127.0.0.1"
    finally:
        # Close the socket to free up resources
        s.close()
    
    return ip_address

# Print the local IP address of the machine
print(f"The IP address of this machine is: {get_ip_address()}")
