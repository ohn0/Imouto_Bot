from PIL import Image

class asciiConverter:
    grayscaleGradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\"^`\". "
    GRAYSCALE = 'LA'
    img = None
    def __init__(self):
        self.img = None

    def convertToGrayscale(self,filename):
        grayscaleFilename = filename[0:-3]+"_Grayscale."+filename[-3:]
        self.img = Image.open(filename).convert('LA').convert('RGB')
        avenge = Image.open('avenge.png')
        self.img.paste(avenge, (0,0), avenge)
        self.img.save(grayscaleFilename)
        return grayscaleFilename



        