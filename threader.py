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
    urlID = [0]
    totalCount = [0]
    threadLock = threading.Lock()
    uniqueIPs = set()
    uniqueHosts = set()

    # Statistics
    dnslookups = [0]
    robots = [0]
    links = [0]
    bytes = [0]
    status2xx = [0]
    status3xx = [0]
    status4xx = [0]
    status5xx = [0]
    status_o = [0]

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
                return

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
                # self.printInfo(info)
                continue

            ip = connection.getIP(host)
            info.append("\tDoing DNS... " + (("done, found on: " + ip) if ip is not None else "failed") + "\n")


            if ip is not None:
                self.threadLock.acquire()
                self.dnslookups[0] += 1
                self.threadLock.release()

            if ip not in self.uniqueIPs:
                self.uniqueIPs.add(host)

                info.append("\tChecking ip uniqueness... passed\n")  # INFO ADD: Unique Host Passed
            else:
                info.append("\tChecking ip uniqueness... failed\n")  # INFO ADD: Unique Host Failed
                connection.closeSocket()
                # self.printInfo(info)
                continue

            hReq = r.createHEADReq(host)

            info.append("\tConnecting on robots... done\n")  # INFO ADD: Robots

            robot, hInfo = connection.robots(host, port, str.encode(hReq))

            info.append(hInfo)
            info.append("\tVerifying header... " + ("found" if robot else "failed") + "\n")

            if robot:
                self.threadLock.acquire()
                self.robots[0] += 1
                self.threadLock.release()
            else:
                info.append("\tConnecting on page... done" + "\n")
                connection.createSocket()
                gReq = r.createGETReq(host, path, file)
                connected, status, count, size = connection.crawl(host, port, str.encode(gReq))
                info.append("\tLoading... " + ("success" if connected else "failed") + "\n")

                self.threadLock.acquire()
                if status == 2:
                    self.status2xx[0] += 1
                elif status == 3:
                    self.status3xx[0] += 1
                elif status == 4:
                    self.status4xx[0] += 1
                elif status == 5:
                    self.status5xx[0] += 1
                else:
                    self.status_o[0] += 1

                self.bytes[0] += size
                self.links[0] += count
                self.threadLock.release()
            self.printInfo(info)
            # print(self.urlID[0], "\n")

    def printInfo(self, infoString):
        print("".join(infoString))
