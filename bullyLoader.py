import random

class bullyLoader:
    insultList = []

    def __init__(self):
        try:
            insults = open('insults.txt', 'r')
            self.insultList = insults.readlines()
            insults.close()
        except OSError :
            print('unable to open insults.txt, it does not exist in current dictionary')

        
    def getInsult(self):
        return random.choice(self.insultList)