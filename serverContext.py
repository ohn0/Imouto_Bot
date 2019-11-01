import json

class ServerContext():
    serverContexts = None
    connectedClients = None

    def __init__(self, connectedClients):
        with open('serverContext',encoding="utf8") as jsonFile:
            try:
                self.serverContexts = json.load(jsonFile)
            except json.decoder.JSONDecodeError:
                self.serverContexts = {}


        for client in connectedClients:
            if client not in self.serverContexts:
                self.serverContexts[client] = []

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

    def saveContexts(self):
        with open('serverContext','w') as outFile:
            json.dump(self.serverContexts, outFile)

    def insertNewContext(self, ctx):
        self.serverContexts[ctx] = []


