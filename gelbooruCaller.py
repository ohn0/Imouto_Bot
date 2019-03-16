from booruComm import booruComm
from booruLib import booruLib

class gelbooruCaller(booruComm):
    def __init__(self, ctx, args):
        super().__init__(ctx, args)
        self.apicall = booruLib.apiEndpoints[booruLib.GELBOORU]

    def setArgs(self):
        self.splitArgs()

    def makeRequest(self):
        self.resolveResponse()

    def getContent(self):
        content = self.resolveContent()
        return content

    