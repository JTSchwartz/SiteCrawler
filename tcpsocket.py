# tcpsocket.py
# author: Jacob Schwartz (schwartzj1)

# Library imports
import socket, select
from timer import Timer

# Constants
BUFFER = 2048
TIMEOUT = 25


# Class definition
class TCPsocket:

    def __init__(self):
        self.sock = None
        self.host = ""

    # Create Socket
    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            print("Failed to create a TCP socket {}".format(error))
            self.sock = None

    # Get IP from Hostname
    def getIP(self, url):
        self.host = url
        try:
            return socket.gethostbyname(url)
        except socket.gaierror:
            print("Failed to gethostbyname\n")
            return None

    # Function for debugging
    def connect(self, ip, port):
        timer = Timer()

        if self.sock is None or ip is None:
            if self.sock is None:
                print("Sock is empty")

            if ip is None:
                print("IP is empty\n")
            return
        try:
            with timer.timeout():
                self.sock.connect((ip, port))
                print("Connection Successful: ", ip + "\n")
        except socket.error as error:
            print("Connection Failed {}".format(error))
            self.sock.close()
            self.sock = None

    def crawl(self, host, port, request):

        ip = self.getIP(host)

        if self.sock is None or ip is None or request is None:
            print("One of the necessary parameters is missing");

        try:
            self.sock.connect((ip, port))
            print("Successfully connected to", host, "(", ip, ") on port", port, "\n\nrecv_string:")
            self.sock.send(request)
            response = self.sock.recv(4096)
            while len(response) > 0:
                print(response.decode())
                response = self.sock.recv(4096)
        except socket.error as error:
            print("Connection Failed {}".format(error))
        finally:
            self.sock.close()
            self.sock = None
