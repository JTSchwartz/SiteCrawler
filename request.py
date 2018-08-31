# request.py
# author: Jacob Schwartz (schwartzj1)


class Request:
    """HTTP Requests"""

    def __init__(self):
        self.req = ''

    def getReq(self, host, path, file):
        """Build GET Request"""

        self.req = 'GET ' + path + file + ' HTTP/1.0\nHost: ' + host + '\nConnection: close\n\n'
        return self.req

    def headReq(self, host):
        """Build HEAD Request, checks for robots.txt"""

        self.req = 'HEAD /robots.txt HTTP/1.0\nHost:' + host + '\n\n'
        return self.req
