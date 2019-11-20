import json

class ServerContext():
    serverContexts = None
    connectedClients = None
    contextKeys = [
        "clients",
        "users",
        "userStats",
        "filter",
        "insults",
        "config"
    ]

    def __init__(self, connectedClients):
        with open('serverContext',encoding="utf8") as jsonFile:
            try:
                self.serverContexts = json.load(jsonFile)
                self.updateContexts()
                self.updateContextConfig()
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
            "insults":[],
            "config":{
                "disgust" : False,
            }
        }

    def getContext(self):
        # print(self.serverContexts)
        return self.serverContexts

    def getFilter(self, ctx):
        return self.serverContexts[ctx]["filter"]

    def updateContexts(self):
        for context in self.serverContexts:
            for key in self.contextKeys:
                if key not in self.serverContexts[context]:
                    # print(key)
                    if key == "users" or key == "userStats":
                        self.serverContexts[context][key] = {}
                    elif key == "config":
                        self.serverContexts[context][key] = {
                            "disgust" : False,
                        }
                    else:
                        self.serverContexts[context][key] = []

    def getServers(self):
        contexts = []
        for context in self.serverContexts:
            contexts.append(context)

        return contexts

    def updateContextConfig(self):
        for context in self.serverContexts:
            if "disgust" not in self.serverContexts[context]["config"]:
                self.serverContexts[context]["config"]["disgust"] = False               
            elif "piss" not in self.serverContexts[context]["config"]:
                self.serverContexts[context]["config"]["piss"] = False
            elif "loli" not in self.serverContexts[context]["config"]:
                self.serverContexts[context]["config"]["loli"] = False


    def toggleContextConfig(self, ctx, configKey):
        self.serverContexts[ctx]["config"][configKey] = not self.serverContexts[ctx]["config"][configKey]
        return self.serverContexts[ctx]["config"][configKey]

    def getContextConfigKeyValue(self, ctx, configKey):
        return self.serverContexts[ctx]["config"][configKey]                                                                    


