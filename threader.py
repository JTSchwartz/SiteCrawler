# threader.py
# author: Jacob Schwartz (schwartzj1)
from collections import Set
from queue import Queue
import threading
from request import Request
from tcpsocket import TCPsocket
from urlparser import URLparser


class Threader(threading.Thread):

    urls = Queue()
    urlID = [1]
    totalCount = [1]
    threadLock = threading.Lock()
    uniqueIPs = set()
    uniqueHosts = set()

    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.id = threadID
        self.urls = q
        self.totalCount[0] = q.qsize()

    def run(self):
        info = [""]
        url = [""]
        connection = TCPsocket()

        while True:
            self.threadLock.acquire()

            if self.urlID[0] > self.totalCount[0]:
                self.threadLock.release()
                break

            url[0] = self.urls.get()
            self.urlID[0] += 1
            info.append("\nURL: " + url[0])  # INFO ADD: URL
            self.threadLock.release()

            urlParse = URLparser()
            r = Request()
            host, port, path, file = urlParse.parse(url[0])
            info.append("\tParsing URL... host " + host + ", port " + str(port) + "\n")  # INFO ADD: Host and Port
            connection.createSocket()

            if host not in self.uniqueHosts:
                self.uniqueHosts.add(host)

                info.append("\tChecking host uniqueness... passed\n")  # INFO ADD: Unique Host Passed
            else:
                info.append("\tChecking host uniqueness... failed\n")  # INFO ADD: Unique Host Failed
                connection.closeSocket()
                self.printInfo(info)
                return

            ip = connection.getIP(host)
            info.append("\tDoing DNS... " + (("done, found on: " + ip) if ip is not None else "failed") + "\n")

            if ip not in self.uniqueIPs:
                self.uniqueIPs.add(host)

                info.append("\tChecking ip uniqueness... passed\n")  # INFO ADD: Unique Host Passed
            else:
                info.append("\tChecking ip uniqueness... failed\n")  # INFO ADD: Unique Host Failed
                connection.closeSocket()
                self.printInfo(info)
                return

            hReq = r.createHEADReq(host)

            info.append("\tConnecting on robots... done\n")  # INFO ADD: Robots

            robots, hInfo = connection.robots(host, port, str.encode(hReq))

            info.append(hInfo)
            info.append("\tVerifying header... " + ("found" if robots else "failed") + "\n")

            if not robots:
                info.append("\tConnecting on page... done" + "\n")
                connection.createSocket()
                gReq = r.createGETReq(host, path, file)
                info.append("\tLoading... " + ("success" if connection.crawl(host, port, str.encode(gReq)) else "failed") + "\n")

            self.printInfo(info)

    def printInfo(self, infoString):
        print("".join(infoString))
