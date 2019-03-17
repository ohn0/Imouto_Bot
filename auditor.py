class Auditor:
    textFile = None
    auditLines = []
    filename = ""

    def __init__(self, filename):
        self.filename = filename

    def generateAuditLog(self):
        self.textFile = open(self.filename, 'r')
        self.auditLines = self.textFile.readlines()
        self.textFile.close()

    def audit(self, author, file_url, tags):
        self.textFile = open(self.filename, 'a')
        self.textFile.write(author + ", " + tags + ", " + file_url + "\n")
        self.closeFile()

    def getInitialAuditLog(self):
        return self.auditLines

    def closeFile(self):
        self.textFile.close()