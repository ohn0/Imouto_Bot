class Auditor:
    textFile = None
    filename = ""

    def __init__(self, filename):
        self.filename = filename

    def audit(self, author, file_url, tags):
        self.textFile = open(self.filename, 'a')
        self.textFile.write(author + ", " + tags + ", " + file_url + "\n")
        self.closeFile()

    def closeFile(self):
        self.textFile.close()