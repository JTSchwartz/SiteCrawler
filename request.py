# request.py
# author: Jacob Schwartz (schwartzj1)


class Request:
    """HTTP Requests"""

    def __init__(self):
        self.req = ''

    def createGETReq(self, host, path, file):
        """Build GET Request"""

        self.req = 'GET ' + path + file + ' HTTP/1.0\nUser-agent: udaytoncrawler/1.0\nHost: ' + host + '\nConnection: close\n\n'
        return self.req

    def createHEADReq(self, host):
        """Build HEAD Request, checks for robots.txt"""

        self.req = 'HEAD /robots.txt HTTP/1.0\nUser-agent: udaytoncrawler/1.0\nHost:' + host + '\n\n'
        return self.req
