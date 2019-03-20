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

    def audit(self, author, file_url, tags):
        self.textFile = open(self.filename, 'a')
        self.textFile.write(author + ", " + tags + ", " + file_url +  "\n")
        self.previousAudit["author"] = author
        self.previousAudit["file_url"] = file_url
        self.previousAudit["tags"] = tags
        self.closeFile()

    def getInitialAuditLog(self):
        return self.auditLines

    def closeFile(self):
        self.textFile.close()

    def getLastAudit(self):
        return self.previousAudit