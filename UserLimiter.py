from UserStatTracker import UserStatTracker
import datetime

class UserLimiter:
    users = None
    userTimers = {}
    def __init__(self):
        self.users = None

    def limitUser(self, user):
        tUser = user
        self.userTimers[tUser] = datetime.datetime.now()

    def checkIfLimited(self, user):
        if not any(self.userTimers):
            return False            
        tUser = user
        tDelta = abs(self.userTimers[tUser] - datetime.datetime.now())
        if tDelta.seconds > 5:
            del self.userTimers[tUser]
            return False
        else:
            return True

