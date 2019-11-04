class CustomInsults():
    serverContexts = {}
    def __init__(self, serverContexts):
        for ctx in serverContexts:
            self.serverContexts[ctx] = serverContexts[ctx]["insults"]


    def getInsultContext(self, clientID):
        return self.serverContexts[clientID]

    def addInsultContext(self, insult, clientID):
        if insult not in self.serverContexts[clientID]:
            self.serverContexts[clientID].append(insult)
            return True
        return False

    def deleteInsultContext(self, insultIndex, clientID):
        try:
            # print(self.serverContexts[clientID])
            del self.serverContexts[clientID][insultIndex]
            return True
        except IndexError:
            return False

    def saveContexts(self, serverContext):
        serverContext.saveContexts(self.serverContexts, "insults")
    