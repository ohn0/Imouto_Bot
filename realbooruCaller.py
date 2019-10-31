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
            auditMessages = []
            for v in range(self.modularValue):
                imageNum = random.randint(0,self.randPost)
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
