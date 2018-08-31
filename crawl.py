# crawl.py
# author: Jacob Schwartz (schwartzj1)

# Import classes
from queue import Queue
from request import Request
from tcpsocket import TCPsocket
from urlparser import URLparser


# Main function
def main() :
    q = Queue()
    print("# of URLs: ", q.qsize())
    urlParse = URLparser()
    r = Request()
    connection = TCPsocket()

    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                q.put(line)
    except IOError:
        print("File does not exist")
        exit(1)

    count = 0

    while not q.empty():
        url = q.get()
        count += 1
        print(count)
        print("URL: ", url)
        host, port, path, file = urlParse.parse(url)
        request = r.getReq(host, path, file)
        print("Request: ", request)
        connection.connect(connection.getIP(host), port)
        # connection.connect(host, port, request)


if __name__ == "__main__":
    main()
