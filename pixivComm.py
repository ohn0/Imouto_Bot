from pixivapi import Client, enums
from random import randint
import pathlib
import glob

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
        print(dir(randIllust))
        while randIllust.type != enums.ContentType.ILLUSTRATION:
            randIllust = illustrations[randint(0,len(illustrations) - 1)]
    
        self.getImage(randIllust)
        imageURL =  randIllust.image_urls[enums.Size.ORIGINAL]
        imageURL = glob.glob("./pixiv/" + str(randIllust.id) + "*")[0]
        return imageURL

    def getImage(self, illustration):
        illustration.download(pathlib.Path("./pixiv", size=enums.Size.ORIGINAL), filename = illustration.id)

    def testFetch(self):
        self.pixivClient.authenticate(self.token)
        illus = self.pixivClient.fetch_illustration(82417326)
        self.getImage(illus)