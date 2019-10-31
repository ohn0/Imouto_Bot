from booruLib import booruLib
from TagStatTracker import tag, TagStatTracker
import responseAuditor
import discord
from discord.ext import commands
import os
import asyncio
import requests
import random
import json


class booruComm:
    argList = []
    randPost = 0
    tagList = ""
    ctx = None
    params = []
    imageReturned = True
    sendTags = False
    apicall = ""
    response = None
    responseAuditor = None

    def __init__(self, ctx, args):
        self.argList = args.split(" ")
        self.tagLogger = []
        self.randPost = random.randint(0, 50)
        self.imageReturned = True
        self.sendTags = False
        self.usePages = False
        self.modularLoading = False
        self.modularValue = 1
        self.tags = ""
        self.ctx = ctx
        self.params = []
        self.instance = ""
        self.responseAuditor = responseAuditor.ResponseAuditor("responseAuditor")

    def splitArgs(self):
        for arg in self.argList:
            if(not arg.startswith('--')):
                self.tagList = arg + "+" + self.tagList
                self.tagLogger.append(arg)
            else:
                if arg[0:-1] == '--numb':
                    self.modularLoading = True
                    self.modularValue = int(arg[-1])
                else:
                    self.params.append(arg)

        for param in self.params:
            if param == '--tags':
                self.sendTags = True
            elif param == '--pages':
                self.usePages = True

        tagEntry = TagStatTracker()
        tagEntry.updateTagFile(tag(self.tagLogger, self.instance,str(self.ctx.message.author)))

        self.tagList = self.tagList[0: len(self.tagList)-1]

    def auditEntireResponse(self):
        self.responseAuditor.auditResponse(self.response, str(self.ctx.message.author))

    def resolveResponse(self):
        try:
            self.apicall += "200&json=1&tags="+self.tagList
            self.response = requests.get(self.apicall)
            self.response = self.response.json()
            responseLength = len(self.response)
            if responseLength == 0:
                self.imageReturned = False
            else:
                print(responseLength)
                self.randPost = random.randint(0, responseLength-1)
        except json.decoder.JSONDecodeError:
            self.imageReturned = False

    def getResponse(self):
        return self.response

    def validateResponse(self):
        if len(self.response) == 0:
            self.imageReturned = False
            return False
        return True

    def resolveContent(self):
        if self.imageReturned:
            auditMessages = []
            for v in range(self.modularValue):
                self.randPost = random.randint(0,self.randPost)
                auditMessages.append({
                    "message":self.response[self.randPost]['file_url'],
                    "tags":self.response[self.randPost]['tags'],
                    "response": self.ctx.message.author.mention + ", Here's your image, big brother! " + self.response[self.randPost]['file_url']
                })
                # auditMessages.append(self.response[self.randPost]['file_url'])
                # auditMessages.append(self.response[self.randPost]['tags'])
            imageNum = self.randPost#random.randint(0, self.randPost - 1)
            responseMessage = self.ctx.message.author.mention + ", Here's your image, big brother! " + self.response[imageNum]['file_url']
            self.tags = self.response[imageNum]['tags']
            return { 
                     "sendTags": self.sendTags,
                     "tags" : self.tags, 
                    #  "auditMessage": [
                    #      str(self.response[imageNum]['file_url']),
                    #      str(self.response[imageNum]['tags'])
                    #  ]
                     "auditMessage":auditMessages,
                     "values":self.modularValue
                     }
        else:
            return None
            




