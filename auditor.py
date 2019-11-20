import datetime

class Auditor:
    textFile = None
    auditLines = []
    filename = ""
    responseAuditor = None
    previousAudit = {"author": None,
                     "file_url": None,
                     "tags": None}

    contextAudits = {

    }                 
    


    def __init__(self, filename):
        self.filename = filename

    def generateAuditLog(self):
        self.textFile = open(self.filename, 'r', encoding="utf8")
        self.auditLines = self.textFile.readlines()
        self.textFile.close()

    def populateServerInfo(self, servers):
        for server in servers:
            self.contextAudits[server] = {
                "author": None,
                "file_url": None,
                "tags": None
            }

    def audit(self, author, file_url, tags, serverContext, auditSource = "n/a"):
        auditObj = {
            "author":author,
            "file_url": file_url,
            "tags": tags,
            "source": auditSource
        }
        self.privateAudit(auditObj)
        self.updatePreviousAudit(auditObj, serverContext)

        # self.textFile = open(self.filename, 'a')
        # self.textFile.write(author + ", " + tags + ", " + file_url + ", " +  str(datetime.datetime.now()) + ", " +  auditSource  + "\n")
        # self.closeFile()

        ##the region below should be refactored
        # self.previousAudit["author"] = author
        # self.previousAudit["file_url"] = file_url
        # self.previousAudit["tags"] = tags

    def privateAudit(self, auditObj):
        self.textFile = open(self.filename, 'a')
        self.textFile.write(auditObj["author"] + ", " + auditObj["tags"] + ", " + auditObj["file_url"] + ", " + str(datetime.datetime.now()) + ", " + auditObj["source"] + "\n")
        # self.textFile.write(author + ", " + tags + ", " + file_url + ", " +  str(datetime.datetime.now()) + ", " +  auditSource  + "\n")
        self.closeFile()
 
    def getInitialAuditLog(self):
        return self.auditLines

    def closeFile(self):
        self.textFile.close()

    def getLastAudit(self, serverID):
        return self.contextAudits[serverID]

    def updatePreviousAudit(self, auditObj, context):

        # self.contextAudits[context] = {
        #     "author":author,
        #     "URL": file_url,
        #     "tags": tags,
        #     "source": auditSource
        # }

        self.contextAudits[context]["author"] = auditObj["author"]
        self.contextAudits[context]["file_url"] = auditObj["file_url"]
        self.contextAudits[context]["tags"] = auditObj["tags"] 

        self.previousAudit["author"] = auditObj["author"]
        self.previousAudit["file_url"] = auditObj["file_url"]
        self.previousAudit["tags"] = auditObj["tags"]

    def insertNewContext(self, context):
        self.contextAudits[context] = {
            "author": None,
            "file_url": None,
            "tags": None
        }
            