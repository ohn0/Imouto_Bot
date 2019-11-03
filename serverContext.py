import json

class ServerContext():
    serverContexts = None
    connectedClients = None
    contextKeys = [
        "clients",
        "users",
        "userStats",
        "filter",
        "insults"
    ]

    def __init__(self, connectedClients):
        with open('serverContext',encoding="utf8") as jsonFile:
            try:
                self.serverContexts = json.load(jsonFile)
                self.updateContexts()
            except json.decoder.JSONDecodeError:
                self.serverContexts = {}


        for client in connectedClients:
            if client not in self.serverContexts:
                self.insertNewContext(client)

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

    def saveContexts(self, contexts, contextType):
        for ctx in contexts:
            self.serverContexts[ctx][contextType] = contexts[ctx]

    def writeContextsToFile(self):
        with open('serverContext', 'w') as outFile:
            json.dump(self.serverContexts, outFile)


    def insertNewContext(self, ctx):
        self.serverContexts[ctx] = {
            "clients":[],
            "users":{},
            "userStats":{},
            "filter":[],
            "insults":[]
        }

    def getContext(self):
        print(self.serverContexts)
        return self.serverContexts

    def getFilter(self, ctx):
        return self.serverContexts[ctx]["filter"]

    def updateContexts(self):
        for context in self.serverContexts:
            for key in self.contextKeys:
                if key not in self.serverContexts[context]:
                    print(key)
                    if key == "users" or key == "userStats":
                        self.serverContexts[context][key] = {}
                    else:
                        self.serverContexts[context][key] = []                                        


