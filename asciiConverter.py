from PIL import Image

class asciiConverter:
    grayscaleGradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\"^`\". "
    GRAYSCALE = 'LA'
    img = None
    def __init__(self):
        self.img = None

    def convertToGrayscale(self,filename):
        extension = ''
        if filename[-4:] == 'jpeg':
            extension = filename[-4:]
        else:
            extension = filename[-3:]
        grayscaleFilename = filename[0:-4]+"_Grayscale."+extension
        self.img = Image.open(filename).convert('LA').convert('RGB')
        # avenge = Image.open('avenge.png')
        # self.img.paste(avenge, (0,0), avenge)
        # self.img.save(grayscaleFilename)
        self.img.save(grayscaleFilename)
        return grayscaleFilename

    def applyAvengerTemplate(self, filename):
        # avengeTemplate = Image.open('avenge.png')
        grayscaleImg = self.convertToGrayscale(filename)
        self.img = Image.open(grayscaleImg)
        avengeTemplate = self.resizeAvengeTemplate(self.img.size)
        self.img.paste(avengeTemplate, (0,0), avengeTemplate)
        self.img.save(grayscaleImg)
        return grayscaleImg

    def resizeAvengeTemplate(self, nImageRatio):
        avengeTemplate = Image.open('avenge.png')
        # nWidth, nHeight = nImage.size
        aWidth, aHeight = avengeTemplate.size

        # nRatio = nWidth / nHeight
        aWidth = aWidth * (nImageRatio[0] / (float)(aWidth))
        aHeight = aHeight * (nImageRatio[1] / (float)(aHeight))

        avengeTemplate = avengeTemplate.resize(((int)(aWidth), (int)(aHeight)), Image.ANTIALIAS)

        return avengeTemplate
    


        