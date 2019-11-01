class Filter():
    filteredWords = []
    contextWordBanner = None
    def __init__(self):
        filterFile = open('filter.txt', 'r')
        for f in filterFile:
            self.filteredWords.append(f[0:-1])
        filterFile.close()

    def getBannedWords(self):   
        return self.filteredWords

    def isArgClean(self, args):
        for arg in args:
            if arg in self.filteredWords:
                return False
        return True

    def isArgCustomBanned(self, args, customBans):
        for arg in args:
            if arg in customBans:
                return True
        return False

    