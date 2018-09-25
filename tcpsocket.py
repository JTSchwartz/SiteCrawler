# tcpsocket.py
# author: Jacob Schwartz (schwartzj1)

# Library imports
import re
import socket
from request import Request
from urlparser import URLparser

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
        except UnicodeError:
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
        href = 0
        size = 0
        # pagelinks = list()

        if self.sock is None or ip is None or request is None:
            self.closeSocket()
            return found, status, href, size

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

            size = len(getResponse.encode('utf-8'))

            if "HTTP/1.0 2" in getResponse or "HTTP/1.1 2" in getResponse:
                # regex = re.compile('(?<=href=").*?(?=")')
                found = True
                # pagelinks = regex.findall(getResponse)
                # href += len(pagelinks)
                href += getResponse.count("href=")
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

        return found, status, href, size

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

    # Used for testing how many extracted links return with status 200 OK. Not used in final project
    def linkStatus(self, url):

        urlParse = URLparser()
        r = Request()

        host, port, path, file = urlParse.parse(url)

        request = r.createGETReq(host, path, file)
        ip = self.getIP(host)
        found = False

        self.createSocket()

        if self.sock is None or ip is None or request is None:
            self.closeSocket()
            return found

        gReq = str.encode(request)

        try:
            self.sock.settimeout(5.0)
            self.sock.connect((ip, port))
            self.sock.send(gReq)
            response = self.sock.recv(4096)
            getList = []
            while len(response) > 0:
                getList.append(response.decode("utf-8", "ignore"))
                response = self.sock.recv(4096)

            getResponse = "".join(getList)
            # print(getResponse)

            if "HTTP/1.0 2" in getResponse or "HTTP/1.1 2" in getResponse:
                found = True
        except socket.error as error:
            found = False
        finally:
            self.closeSocket()

        return found

    def closeSocket(self):
        self.sock.close()
        self.sock = None