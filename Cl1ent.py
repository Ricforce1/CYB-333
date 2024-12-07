
import socket
import sys

# Constants
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.44"
ADDR = (SERVER, PORT)

def create_connection():
    """Create and return a socket connection to the server"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"Connected to server at {SERVER}:{PORT}")
        return client
    except ConnectionRefusedError:
        print("Connection failed. Make sure the server is running.")
        sys.exit(1)
    except socket.error as e:
        print(f"Socket error occurred: {e}")
        sys.exit(1)

def send_message(client_socket, msg):
    """Send a message to the server with proper header"""
    try:
        # Encode the message
        message = msg.encode(FORMAT)
        msg_length = len(message)
        
        # Prepare and send the header
        send_length = str(msg_length).encode(FORMAT)
        send_length = send_length + b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        
        # Send the actual message
        client_socket.send(message)
        print(f"Sent message: {msg}")
        
        # Wait for server acknowledgment
        try:
            response = client_socket.recv(2048).decode(FORMAT)
            print(f"Server response: {response}")
        except socket.timeout:
            print("No response from server")
            
    except socket.error as e:
        print(f"Error sending message: {e}")
        return False
    return True

def main():
    # Create connection
    client = create_connection()
    
    # Set a timeout for receiving responses
    client.settimeout(5)
    
    try:
        # Send test messages
        messages = [
            "Hello World!",
            "Hello Everyone!",
            "Hello Buddy!",
            DISCONNECT_MESSAGE
        ]
        
        for msg in messages:
            send_message(client, msg)
            if msg != DISCONNECT_MESSAGE:
                input("Press Enter to send next message...")
                
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        send_message(client, DISCONNECT_MESSAGE)
    finally:
        print("Closing connection...")
        client.close()

if __name__ == "__main__":
    main()