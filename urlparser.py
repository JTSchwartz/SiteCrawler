# urlparser.py
# author: Jacob Schwartz (schwartzj1)


# Parse URL
class URLparser:

    def __init__(self):
        self.host = ""
        self.port = None
        self.path = ""
        self.file = ""

    def parse(self, url):
        backslash = url.index("/")
        colon = url.index(":")
        