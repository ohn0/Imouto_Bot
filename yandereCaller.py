from booruComm import booruComm
from booruLib import booruLib
import requests
import json
import random

class YandereCaller(booruComm):
    def __init__(self, ctx, args):
        super().__init__(ctx, args)
        self.apicall = booruLib.apiEndpoints[booruLib.YANDERE]
        self.instance = "YANDERE"
        self.filteredTags = "+-loli+-lolicon+-shotacon+-guro+-bestiality"

    def setArgs(self):
        self.splitArgs()

    def resolveResponse(self, extremeFilteringEnabled):
        try:
            if extremeFilteringEnabled:
                self.apicall += "200&tags="+self.tagList+self.filteredTags
            else:
                self.apicall += "200&tags="+self.tagList
            self.response = requests.get(self.apicall)
            self.response = self.response.json()
            responseLength = len(self.response)
            if responseLength == 0:
                self.imageReturned = False
            else:
                self.randPost = random.randint(0, responseLength-1)
        except json.decoder.JSONDecodeError:
            self.imageReturned = False

    def makeRequest(self, extremeFilteringEnabled = False):
        self.resolveResponse(extremeFilteringEnabled)

    def getContent(self):
        content = self.resolveContent()
        return content