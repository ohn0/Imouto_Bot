class CustomFilter():
    serverContexts = {}
    def __init__(self, serverContexts):
        for ctx in serverContexts:
            print(ctx)
            self.serverContexts[ctx] = serverContexts[ctx]["filter"]

    def getBanContext(self, clientID):
        return self.serverContexts[clientID]

    def banWordContext(self, word,clientID):
        if word not in self.serverContexts[clientID]:
            self.serverContexts[clientID].append(word)
            return True
        else:
            return False

    def unbanWordContext(self, word,clientID):
        if word in self.serverContexts[clientID]:
            self.serverContexts[clientID].remove(word)
            return True
        else:
            return False


    def saveContexts(self, serverContext):
        serverContext.saveContexts(self.serverContexts, "filter")

    def insertNewContext(self, context):
        self.serverContexts[context] = []