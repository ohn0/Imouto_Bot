import datetime

class TagStatTracker:
    tagStats = {}
    tagFile = None

    def __init__(self):
        self.tagFile = None

    def updateTagFile(self, tag):
        self.tagFile = open("tag.txt", 'a')
        self.tagFile.write(str(tag.tag["tag"]) + "\t" + str(tag.tag["site"] + "\t" + tag.tag["requestor"]+ str(datetime.datetime.now())+ "\n"))
        self.tagFile.close()

    
class tag:
    tag = {
        "tag" : None,
        "site": None,
        "requestor": None
    }

    def __init__(self, tags, site, requestor):
        self.tag["tag"] = tags
        self.tag["site"] = site
        self.tag["requestor"] = requestor