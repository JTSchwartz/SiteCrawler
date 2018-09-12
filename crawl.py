# crawl.py
# author: Jacob Schwartz (schwartzj1)

# Import classes
from queue import Queue
from request import Request
from tcpsocket import TCPsocket
from urlparser import URLparser


# Main function
def main():
    q = Queue()
    connection = TCPsocket()

    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                q.put(line)
    except IOError:
        print("File does not exist")
        exit(1)

    print("# of URLs: ", q.qsize(), "\n")
    count = 0

    while not q.empty():
        urlParse = URLparser()
        r = Request()
        url = q.get()
        count += 1
        print("\n-----------\nURL#:", count, "(", url.rstrip("\n"), ")\n")
        connection.createSocket()
        host, port, path, file = urlParse.parse(url)
        hReq = r.createHEADReq(host)

        if not connection.robots(host, port, str.encode(hReq)):
            connection.createSocket()
            gReq = r.createGETReq(host, path, file)
            connection.crawl(host, port, str.encode(gReq))


if __name__ == "__main__":
    main()
