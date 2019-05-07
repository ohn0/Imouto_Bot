import datetime
class Auditor:
    textFile = None
    auditLines = []
    filename = ""
    previousAudit = {"author": None,
                     "file_url": None,
                     "tags": None}

    def __init__(self, filename):
        self.filename = filename

    def generateAuditLog(self):
        self.textFile = open(self.filename, 'r')
        self.auditLines = self.textFile.readlines()
        self.textFile.close()

    def audit(self, author, file_url, tags, auditSource = "n/a"):
        auditObj = {
            "author":author,
            "URL": file_url,
            "tags": tags,
            "source": auditSource
        }
        self.privateAudit(auditObj)
        self.updatePreviousAudit(auditObj)

        # self.textFile = open(self.filename, 'a')
        # self.textFile.write(author + ", " + tags + ", " + file_url + ", " +  str(datetime.datetime.now()) + ", " +  auditSource  + "\n")
        # self.closeFile()

        ##the region below should be refactored
        # self.previousAudit["author"] = author
        # self.previousAudit["file_url"] = file_url
        # self.previousAudit["tags"] = tags

    def privateAudit(self, auditObj):
        self.textFile = open(self.filename, 'a')
        self.textFile.write(auditObj["author"] + ", " + auditObj["tags"] + ", " + auditObj["URL"] + ", " + str(datetime.datetime.now()) + ", " + auditObj["source"] + "\n")
        # self.textFile.write(author + ", " + tags + ", " + file_url + ", " +  str(datetime.datetime.now()) + ", " +  auditSource  + "\n")
        self.closeFile()

    def getInitialAuditLog(self):
        return self.auditLines

    def closeFile(self):
        self.textFile.close()

    def getLastAudit(self):
        return self.previousAudit

    def updatePreviousAudit(self, auditObj):
        self.previousAudit["author"] = auditObj["author"]
        self.previousAudit["file_url"] = auditObj["URL"]
        self.previousAudit["tags"] = auditObj["tags"]