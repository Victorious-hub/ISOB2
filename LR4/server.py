import socket
import time
import threading
import argparse

syn_counts = {}
ack_counts = {}

connection_attempts = {}
flood_protection_enabled = True


def handle_server_connection(client_socket, client_address):
    """
    Handles incoming server connections, checks for flood attacks, and responds to clients.
    Args:
        client_socket (socket.socket): The client socket object.
        client_address (tuple): The client address (IP, port).
    """
    ip = client_address[0]

    if flood_protection_enabled:
        if is_ack_flood(ip):
            print(f"ACK flood detected from {ip}")
        elif is_syn_flood(ip):
            print(f"SYN flood detected from {ip}")
        else:
            print(f"No flood detected from {ip}")

        if not prevent_flood(ip):
            print(f"Connection from {ip} blocked due to potential flood attack")
            client_socket.close()
            return

    print(f"Accepted connection from {ip}")
    client_socket.send(b"ACK")
    client_socket.close()


def prevent_flood(ip):
    """
    Prevents SYN flood and ACK flood attacks by tracking connection attempts.

    Args:
        ip (str): The IP address of the client.

    Returns:
        bool: True if the connection is allowed, False if it is blocked.
    """
    current_time = time.time()
    if ip in connection_attempts:
        connection_attempts[ip].append(current_time)
        connection_attempts[ip] = [t for t in connection_attempts[ip] if current_time - t < 10]

        if len(connection_attempts[ip]) > 10:
            print(f"Potential SYN flood attack from {ip}")
            return False
    else:
        connection_attempts[ip] = [current_time]
    return True

def is_ack_flood(ip):
    """
    Detects ACK flood attacks based on frequent ACK packets.
    Args:
        ip (str): The IP address of the client.

    Returns:
        bool: True if an ACK flood attack is detected, False otherwise.
    """
    current_time = time.time()
    if ip in ack_counts:
        ack_counts[ip] = [t for t in ack_counts[ip] if current_time - t < 1]
        if len(ack_counts[ip]) > 10:
            return True
    else:
        ack_counts[ip] = []
    
    ack_counts[ip].append(current_time)
    return False

def is_syn_flood(ip):
    """
    Detects SYN flood attacks based on frequent SYN packets.

    Args:
        ip (str): The IP address of the client.

    Returns:
        bool: True if a SYN flood attack is detected, False otherwise.
    """
    current_time = time.time()
    if ip in syn_counts:

        syn_counts[ip] = [t for t in syn_counts[ip] if current_time - t < 2]
        if len(syn_counts[ip]) > 5:
            return True
    else:
        syn_counts[ip] = []
    syn_counts[ip].append(current_time)
    return False

def start_server():
    """
    Starts the server to listen for incoming TCP connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9991))
    server_socket.listen(5)  # Listen for up to 5 incoming connections
    print("Server listening on port 9991")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection attempt from {client_address}")
        threading.Thread(target=handle_server_connection, args=(client_socket, client_address)).start()

def parse_arguments():
    """
    Parses command-line arguments to enable or disable flood protection.
    """
    global flood_protection_enabled
    parser = argparse.ArgumentParser(description="Start the server with flood protection settings.")
    parser.add_argument(
        "--flood_protection", choices=["on", "off"], default="on",
        help="Enable or disable flood protection. Default is 'on'."
    )

    args = parser.parse_args()

    # Set flood protection flag based on the argument
    if args.flood_protection == "off":
        flood_protection_enabled = False
        print("Flood protection is DISABLED.")
    else:
        flood_protection_enabled = True
        print("Flood protection is ENABLED.")

if __name__ == "__main__":
    parse_arguments()  # Parse command-line arguments
    server_thread = threading.Thread(target=start_server)
    server_thread.start()