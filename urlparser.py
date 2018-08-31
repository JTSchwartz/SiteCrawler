# urlparser.py
# author: Jacob Schwartz (schwartzj1)
# example url: scheme://[user:pass@] host[:port][/path][?query][#fragment]


# Parse URL
class URLparser:

    def __init__(self):
        self.host = ""
        self.port = 80
        self.path = ""
        self.file = ""

    def parse(self, url):
        url = self.removeProt(url);
        backslash = url.index("/")
        colon = url.index(":")
        qmark = url.index("?")

        bExist, cExist, qExist = self.exist(backslash, colon, qmark)

        # Host
        if cExist:
            self.host = url[:colon]
        elif bExist:
            self.host = url[:backslash]
        elif qExist:
            self.host = url[:qmark]
        else:
            return url, self.port, self.path, self.file

        # Port
        if cExist and bExist > 0:
            self.port = url[colon + 1:backslash]
        elif cExist and qExist > 0:
            self.port = url[colon + 1:qmark]
        elif cExist > 0:
            self.port = url[colon:]

        # Path
        if bExist and qExist:
            self.path = url[backslash:qmark]
        elif bExist:
            self.path = url[backslash:]

        # File
        if qExist:
            self.file = url[qmark:]

        return self.host, self.port, self.path, self.file

    def exist(self, b, c, q):
        return b > 0, c > 0, q > 0

    def removeProt(self, url):
        x = url.index("//")
        return url[x + 2:]
