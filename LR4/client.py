import socket

def main():
    """
    This function creates a TCP client that connects to a server at a specified IP address and port.
    It receives a response from the server, prints the response, and then closes the connection.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9991))
    response = client.recv(4096)
    print(response.decode())
    client.close()

if __name__ == "__main__":
    main()