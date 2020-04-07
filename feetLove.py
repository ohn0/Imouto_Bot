from PIL import Image
from math import floor


def loveFeet():
    rat = Image.open('feet.png')
    test = Image.open('test.jpg')

    resizedTest = test.resize((235,153))
    ratCopy = rat.copy()
    ratCopy.paste(resizedTest)
    ratCopy.save('ratCopy.jpg')


loveFeet()