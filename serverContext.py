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
        self.serverContexts[clientID].append(word)

    def unbanWordContext(self, word,clientID):
        self.serverContexts[clientID].remove(word)

    def saveContexts(self):
        with open('serverContext','w') as outFile:
            json.dump(self.serverContexts, outFile)


