import socket
import threading 

# Constants
HEADER = 64
PORT = 5050
SERVER = "192.168.1.44"  # Make sure this matches your computer's IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            # Receive message length
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())  # Added strip() to remove padding
                msg = conn.recv(msg_length).decode(FORMAT)
                
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"[{addr}] {msg}")
                # Send acknowledgment back to client
                conn.send("Message received".encode(FORMAT))
                
        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False
    
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected")

def start():
    try:
        # Create and bind socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        
        # Start listening
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            # Fixed string formatting and activeCount() to active_count()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
    except socket.error as e:
        print(f"[ERROR] Socket error: {e}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start()