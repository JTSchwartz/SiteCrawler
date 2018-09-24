# crawl.py
# author: Jacob Schwartz (schwartzj1)

# Import classes
import sys
import time
from queue import Queue
from threader import Threader


# Main function
def main(argv):
    start = time.time()

    q = Queue()

    try:
        with open(argv[1]) as file:
            for line in file:
                q.put(line)
    except IOError:
        print("File does not exist")
        exit(1)

    print("# of URLs: ", q.qsize(), "\n")

    threadList = []
    threadCount = int(argv[0])

    for x in range(0, threadCount, 1):
        t = Threader(x, q)
        t.start()
        threadList.append(t)

    for y in threadList:
        y.join()

    pagecount = Threader.status2xx[0] + Threader.status3xx[0] + Threader.status4xx[0] + Threader.status5xx[0] + Threader.status_o[0]
    size = Threader.bytes[0]/1000000

    print("Runtime:", (time.time() - start), "\n"
          "Extracted", Threader.urlID[0], "URLS\n"
          "Looked up", Threader.dnslookups[0], "DNS names\n"
          "Downloaded", Threader.robots[0], "robots\n"
          "Crawled", pagecount, "pages (", size, "MB)\n"
          "Parsed", Threader.links[0], "Links\n"
          "HTTP Codes: 2xx:", Threader.status2xx[0],
          "3xx:", Threader.status3xx[0],
          "4xx:", Threader.status4xx[0],
          "5xx:", Threader.status5xx[0],
          "Other:", Threader.status_o[0])


if __name__ == "__main__":
    main(sys.argv[1:])
