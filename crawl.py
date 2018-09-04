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
    q.put("https://www.jtschwartz.com")

    connection = TCPsocket()

    # try:
    #     with open("URL-input-100.txt") as file:
    #         for line in file:
    #             q.put(line)
    # except IOError:
    #     print("File does not exist")
    #     exit(1)

    # print("# of URLs: ", q.qsize(), "\n")
    count = 0

    while not q.empty():
        urlParse = URLparser()
        r = Request()
        url = q.get()
        count += 1
        print("URL#: ", count, "\n")
        connection.createSocket()
        host, port, path, file = urlParse.parse(url)
        request = r.createGETReq(host, path, file)
        # connection.connect(connection.getIP(host), port)
        connection.crawl(host, port, str.encode(request))


if __name__ == "__main__":
    main()
