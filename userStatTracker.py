class UserStatTracker:
    auditFile = None

    users = []

    def __init__(self, auditFile):
        self.auditFile = open(auditFile, 'r')


    

    