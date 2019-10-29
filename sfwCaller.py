from booruComm import booruComm
from booruLib import booruLib
import random

class sfwCaller(booruComm):
    baseURL = "https://safebooru.org//images/"
    def __init__(self, ctx, args):
        super().__init__(ctx, args)
        self.apicall = booruLib.apiEndpoints[booruLib.SFWBOORU]
        self.instance = "SAFEBOORU"
    def setArgs(self):
        self.splitArgs()

    def makeRequest(self):
        self.resolveResponse()

    def buildURL(self, imageNum):
        response = self.getResponse()
        contentURL = self.baseURL + str(response[imageNum]["directory"])+"/"+str(response[imageNum]["image"])
        return contentURL

    def resolveContent(self):
        if self.imageReturned:
            auditMessages = []
            for v in range(self.modularValue):
                imageNum = random.randint(0,50)
                imageURL = self.buildURL(imageNum)
                auditMessages.append({
                    "message":imageURL,
                    "tags":self.response[imageNum]['tags'],
                    "response": self.ctx.message.author.mention + ", Here's your image, big brother! " + imageURL
                })
                responseMessage = self.ctx.message.author.mention + ", Here's your image, big brother! " + imageURL
            self.tags = self.response[imageNum]['tags']
            return { "response": responseMessage,
                     "sendTags": self.sendTags,
                     "tags" : self.tags, 
                     "auditMessage": auditMessages,
                     "values":self.modularValue}
        else:
            return None

    def getContent(self):
        content = self.resolveContent()
        return content
