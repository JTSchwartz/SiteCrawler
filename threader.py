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
    uniqueHosts = set()

    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.id = threadID
        self.urls = q
        self.totalCount[0] = q.qsize()

    def run(self):
        print("URL from Thread: ", self.urls.qsize())
        url = [""]
        connection = TCPsocket()

        while True:
            self.threadLock.acquire()

            if self.urlID[0] > self.totalCount[0]:
                self.threadLock.release()
                break

            url[0] = self.urls.get()
            self.urlID[0] += 1
            print("Thread: %d | URL %d: %s" % (self.id, self.urlID[0], url[0]))
            self.threadLock.release()

            urlParse = URLparser()
            r = Request()
            host, port, path, file = urlParse.parse(url[0])
            connection.createSocket()
            ip = connection.getIP(host)

            if ip not in self.uniqueHosts:
                self.uniqueHosts.add(ip)

                hReq = r.createHEADReq(host)

                if not connection.robots(host, port, str.encode(hReq)):
                    connection.createSocket()
                    gReq = r.createGETReq(host, path, file)
                    connection.crawl(host, port, str.encode(gReq))
            else:
                connection.closeSocket()

        print("Thread Exiting:", self.id)
