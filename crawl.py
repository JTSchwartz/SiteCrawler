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

    print("Runtime:", (time.time() - start))


if __name__ == "__main__":
    main(sys.argv[1:])
