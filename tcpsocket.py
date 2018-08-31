# tcpsocket.py
# author: Jacob Schwartz (schwartzj1)

# Library imports
import socket, select

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
            print("Failed to gethostbyname")
            return None

    def connect(self, ip, port):
        if self.sock is None or ip is None:
            return
        try:
            self.sock.connect((ip, port))
            print("Connection Successful: ", ip)
        except socket.error as error:
            print("Connection Failed {}".format(error))
            self.sock.close()
            self.sock = None
