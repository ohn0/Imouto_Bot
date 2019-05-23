import datetime

class ResponseAuditor:
    responseFile = None
    filename = ""
    def __init__(self, filename):
        self.filename = filename

    def auditResponse(self, responseContent, author):
        self.responseFile = open(self.filename, 'a', encoding="utf-8")
        auditMessage = str(author) + ", " + str(responseContent) + ", " + str(datetime.datetime.now()) + "\n"
        self.responseFile.write(auditMessage)
        self.responseFile.close()