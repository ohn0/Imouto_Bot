from pixivapi import Client, enums
from random import randint
import pathlib

class pixivComm:
    token = ""
    pixivClient = None
    def __init__(self, pixivCreds):
        self.pixivClient = Client()
        self.pixivClient.login(pixivCreds["user"], pixivCreds["pw"])
        self.token = self.pixivClient.refresh_token

    def searchImage(self, tag):
        self.pixivClient.authenticate(self.token)
        searchStr = tag.replace('_', ' ')
        print(searchStr, tag)

        results = self.pixivClient.search_illustrations(searchStr)
        illustrations = results["illustrations"]
        randIllust = illustrations[randint(0,len(illustrations) - 1)]
        self.getImage(randIllust)
        imageURL =  randIllust.image_urls[enums.Size.LARGE]
        return str(randIllust.id) + '.' + imageURL[len(imageURL) - 3 : len(imageURL)]

    def getImage(self, illustration):
        illustration.download(pathlib.Path("./pixiv"), filename = illustration.id)
