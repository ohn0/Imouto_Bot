import random
class helpResponse:
    responseList = []
    def __init__(self):
        try:
            responses = open('bullyImages.txt', 'r')
            self.responseList = responses.readlines()
            responses.close()
        except OSError:
            print('unable to open bullyImages.txt')

    def getResponseImage(self):
        return random.choice(self.responseList)[0:-1]