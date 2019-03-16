from booruLib import booruLib
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
    def __init__(self, ctx, args):
        self.argList = args.split(" ")
        self.randPost = random.randint(0, 50)
        self.imageReturned = True
        self.sendTags = False
        self.tags = ""
        self.ctx = ctx
        self.params = []

    def splitArgs(self):
        for arg in self.argList:
            if(not arg.startswith('--')):
                self.tagList = arg + "+" + self.tagList
            else:
                self.params.append(arg)

        for param in self.params:
            if param == '--tags':
                self.sendTags = True

        self.tagList = self.tagList[0: len(self.tagList)-1]

    def resolveResponse(self):
        try:
            self.apicall += str(self.randPost)+"&json=1&tags="+self.tagList
            self.response = requests.get(self.apicall)
            self.response = self.response.json()
        except json.decoder.JSONDecodeError:
            self.imageReturned = False

    def getResponse(self):
        return self.response

    def resolveContent(self):
        if self.imageReturned:
            imageNum = random.randint(0, self.randPost - 1)
            responseMessage = self.ctx.message.author.mention + ", Here's your image, big brother! " + self.response[imageNum]['file_url']
            self.tags = self.response[imageNum]['tags']
            return { "response": responseMessage,
                     "sendTags": self.sendTags,
                     "tags" : self.tags, 
                     "auditMessage": [
                         str(self.response[imageNum]['file_url']),
                         str(self.response[imageNum]['tags'])
                     ]}
        else:
            return None
            




