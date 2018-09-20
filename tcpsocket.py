# tcpsocket.py
# author: Jacob Schwartz (schwartzj1)

# Library imports
import socket

# Constants
BUFFER = 2048
TIMEOUT = 25


# Class definition
class TCPsocket:

    status2xx = 0
    status3xx = 0
    status4xx = 0
    status5xx = 0
    statusOther = 0

    def __init__(self):
        self.sock = None
        self.host = ""

    # Create Socket
    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            # print("Failed to create a TCP socket {}".format(error))
            self.sock = None

    # Get IP from Hostname
    def getIP(self, url):
        self.host = url
        try:
            return socket.gethostbyname(url)
        except socket.gaierror:
            # print("Failed to gethostbyname\n")
            return None

    # Function for debugging
    def connect(self, ip, port):

        if self.sock is None or ip is None:
            if self.sock is None:
                print("Sock is empty")

            if ip is None:
                print("IP is empty\n")
            return
        try:
            self.sock.connect((ip, port))
            print("Connection Successful: ", ip + "\n")
        except socket.error as error:
            print("Connection Failed {}".format(error))
            self.sock.close()
            self.sock = None

    def crawl(self, host, port, request):

        ip = self.getIP(host)
        found = False
        status = 0
        href_src = 0

        if self.sock is None or ip is None or request is None:
            self.closeSocket()
            return found

        try:
            self.sock.settimeout(5.0)
            self.sock.connect((ip, port))
            # print("GET request response:")
            self.sock.send(request)
            response = self.sock.recv(4096)
            getList = []
            while len(response) > 0:
                getList.append(response.decode("utf-8", "ignore"))
                response = self.sock.recv(4096)

            getResponse = "".join(getList)
            # print(getResponse)

            href_src += getResponse.count("href=") + getResponse.count("src=")

            if "HTTP/1.0 2" in getResponse or "HTTP/1.1 2" in getResponse:
                found = True
                status = 2
            elif "HTTP/1.0 3" in getResponse or "HTTP/1.1 3" in getResponse:
                status = 3
            elif "HTTP/1.0 4" in getResponse or "HTTP/1.1 4" in getResponse:
                status = 4
            elif "HTTP/1.0 5" in getResponse or "HTTP/1.1 5" in getResponse:
                status = 5
        except socket.error as error:
            found = False
        finally:
            self.closeSocket()

        return found, status, href_src

    def robots(self, host, port, request):

        ip = self.getIP(host)
        found = False
        info = "\tLoading... failed\n"

        if self.sock is None or ip is None or request is None:
            self.closeSocket()
            return found, info

        info = "\tLoading... done\n"

        try:
            self.sock.settimeout(5.0)
            self.sock.connect((ip, port))
            self.sock.send(request)
            response = self.sock.recv(4096)
            headList = []
            while len(response) > 0:
                headList.append(response.decode("utf-8", "ignore"))
                response = self.sock.recv(4096)
            headResponse = "".join(headList)

            # print(headResponse)

            if "200 OK" in headResponse:
                found = True
        except socket.error as error:
            info = "\tLoading... failed\n"
        finally:
            self.closeSocket()

        return found, info

    def closeSocket(self):
        self.sock.close()
        self.sock = None