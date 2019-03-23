import datetime

class Timekeeper:
    startTime = None

    def __init__(self):
        self.startTime = datetime.datetime.now()

    def getUptime(self):
        currentTime = datetime.datetime.now()
        return abs(currentTime - self.startTime)