import os

class ClientConnections:
    connectedClients = []
    clientFilterStatus = {}

    def __init__(self):
        if os.stat('activeservers.txt').st_size != 0:
            self.setupClients()

    def setupClients(self):
        serverFile = open('activeservers.txt', 'r')
        servers = serverFile.readlines()
        for server in servers:
            s = server.split(' ')
            toggleVal = False
            if s[1][0:-1] == '1':
                toggleVal = True
            else:
                toggleVal = False
            self.connectedClients.append(s[0])
            self.clientFilterStatus[s[0]] = toggleVal
        serverFile.close()

    def isChannelFiltered(self, guildID):
        return self.clientFilterStatus[str(guildID)]

    def getConnectedServer(self):
        return self.clientFilterStatus

    def updateConnectedClients(self, clientID):
        sclientID = str(clientID)
        if sclientID in self.connectedClients:
            return False
        self.serverFile = open('activeservers.txt', 'r')
        self.serverFile.write(sclientID + ' 1\n')
        self.serverFile.close()

    def toggleFilter(self, clientID):
        sclientID = str(clientID)
        self.clientFilterStatus[(sclientID)] = not self.clientFilterStatus[(sclientID)]
        return self.clientFilterStatus[(sclientID)]

    def writeServerToggleStatus(self):
        serverFile = open('activeservers.txt', 'w+')
        serverFile.truncate(0)
        for key, value in self.clientFilterStatus.items():
            numVal = ''
            if value == True:
                numVal = '1'
            else:
                numVal = '0'
            serverFile.write(str(key) + ' ' + numVal+'\n')
        serverFile.close()
