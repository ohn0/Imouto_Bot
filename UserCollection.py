class UserCollection:

    users = []
    def __init__(self, auditLines):
        self.populateUsers(auditLines)


    def populateUsers(self, auditLines):
        lines = auditLines
        
        for l in lines:
            splitLine = l.split(',')
            name = splitLine[0]

            if name not in self.users:
                self.users.append(name)

        for i,user in enumerate(self.users):
            self.users[i] = user[0:-5]

    def getUsers(self):
        return self.users


    def insertUser(self, user):
        #The user MUST be the name of the user with their discord tag still attached!
        if user not in self.users:
            self.users.append(user[0:-5])

