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
    # q.put("http://appleseeds.blair.com/t/sale/997-under/pc/69/2664.uts?count=12&i=1&intl=n&q=*&q1=69%7ESale&q2=2664%7E$9.97+%26+Under&q3=2X&rank=rank&sc=Y&store=1&x1=c.t1&x2=c.t2&x3=s.sizenormal")

    connection = TCPsocket()

    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                q.put(line)
    except IOError:
        print("File does not exist")
        exit(1)

    print("# of URLs: ", q.qsize())
    count = 0

    while count < 100:
        urlParse = URLparser()
        r = Request()
        url = q.get()
        count += 1
        print(count)
        connection.createSocket()
        print("URL: ", url)
        host, port, path, file = urlParse.parse(url)
        print("Host: " + host)
        print("Port: ", port)
        print("Path: " + path)
        print("File: " + file)
        request = r.getReq(host, path, file)
        print("Request: ", request)
        connection.connect(connection.getIP(host), port)
        # connection.connect(host, port, request)


if __name__ == "__main__":
    main()
