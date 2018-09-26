Site Crawler - Jacob Schwartz
=====

This program was written for a CPS 470 Computer Networks course. This program uses multithreading to crawl any number of URLs, similar to how search engines such as Google and Yahoo work. Crawling in this case consists of connecting to the hosts, sending a HEAD request, and checking the response for presence of a robots.txt file. If one is not present the program will move forward with sending a GET request. Once the thread has hit the end of its run with it current URL, it will print the trace of what it did, and start over with the next URL in the list, if one exists. Once all queued URLs have been run through, the threads will return to their parent process, and the Runtime statistics, such as length of time to run, number of DNS lookups, robots.txt files found, total size of pages crawled, etc. The URLs that are run through are listed in a text file, each one on its own line. The amount of threads the program uses and what file it reads from are input as command line arguments.

-----

How to run:
1. Create new project in PyCharm (Or your preferred Python IDE)
2. Copy all files into the project folder
3. Run with parameters [# of threads] [file with links]
  - Example: `5000 URL-input-1m.txt`
  
