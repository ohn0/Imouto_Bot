from booruComm import booruComm
from booruLib import booruLib
import random

class realbooruCaller(booruComm):
    baseURL = "https://realbooru.com//images/"
    def __init__(self, ctx, callingInstance, args):
        super().__init__(ctx, args)
        self.apicall = booruLib.apiEndpoints[callingInstance]
        self.instance = callingInstance

        if self.instance == booruLib.R34:
            self.baseURL = "https://rule34.xxx//images/"
        elif self.instance == booruLib.XBOORU:
            self.baseURL = "https://xbooru.com//images/"

    def setArgs(self):
        self.splitArgs()

    def makeRequest(self):
        self.resolveResponse()
        self.auditEntireResponse()


    def buildURL(self, imageNum):
        response = self.getResponse()
        contentURL = self.baseURL + str(response[imageNum]["directory"])+"/"+str(response[imageNum]["image"])
        return contentURL

    def resolveContent(self):
        if self.imageReturned:
            imageNum = self.randPost
            imageURL = self.buildURL(imageNum)
            responseMessage = self.ctx.message.author.mention + ", Here's your image, big brother! " + imageURL
            self.tags = self.response[imageNum]['tags']
            return { "response": responseMessage,
                     "sendTags": self.sendTags,
                     "tags" : self.tags, 
                     "auditMessage": [
                         str(imageURL),
                         str(self.response[imageNum]['tags'])
                     ]}
        else:
            return None

    def getContent(self):
        content = self.resolveContent()
        return content
