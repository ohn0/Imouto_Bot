from PIL import Image
from math import floor

class asciiConverter:
    grayscaleGradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\"^`\". "
    gradientLength = 67
    GRAYSCALE = 'LA'
    img = None
    def __init__(self):
        self.img = None

    def convertToGrayscale(self,imageFile):
        # extension = ''
        # if filename[-4:] == 'jpeg':
        #     extension = filename[-4:]
        # else:
        #     extension = filename[-3:]
        # grayscaleFilename = filename[0:-4]+"_Grayscale."+extension
        # self.img = Image.open(filename).convert('LA').convert('RGB')
        grayscaleImage = imageFile.convert('LA').convert('RGB')
        # # r = self.img.load()
        # self.img.save(grayscaleFilename)
        # self.img.close()
        return grayscaleImage

    def resolveExtension(self, filename):
        extension = ''
        if filename[-4:] == 'jpeg':
            extension = filename[-4:]
        else:
            extension = filename[-3:]

        return extension

    def getGrayscaleFilename(self, filename):
        return filename[0:-4]+"_Grayscale."+self.resolveExtension(filename)

    def createGrayscaleFile(self, filename):
        grayscaleFilename = self.getGrayscaleFilename(filename)
        grayscaleImage = self.createGrayscaleImage(filename)
        grayscaleImage.save(grayscaleFilename)
        return grayscaleFilename

    def createGrayscaleImage(self, filename):
        nonGrayscaleImage = Image.open(filename)
        grayscaleImage = self.convertToGrayscale(nonGrayscaleImage)
        nonGrayscaleImage.close()
        return grayscaleImage

    def applyAvengerTemplate(self, filename):
        grayscaleImg = self.createGrayscaleImage(filename)
        avengeFilename = "avenge"+self.getGrayscaleFilename(filename)
        # self.img = Image.open(grayscaleImg)
        avengeTemplate = self.resizeAvengeTemplate(grayscaleImg.size)
        grayscaleImg.paste(avengeTemplate, (0,0), avengeTemplate)
        grayscaleImg.save(avengeFilename)
        return avengeFilename

    def resizeAvengeTemplate(self, nImageRatio):
        avengeTemplate = Image.open('avenge.png')
        # nWidth, nHeight = nImage.size
        aWidth, aHeight = avengeTemplate.size

        # nRatio = nWidth / nHeight
        aWidth = aWidth * (nImageRatio[0] / (float)(aWidth))
        aHeight = aHeight * (nImageRatio[1] / (float)(aHeight))

        avengeTemplateResized = avengeTemplate.resize(((int)(aWidth), (int)(aHeight)), Image.ANTIALIAS)
        avengeTemplate.close()
        return avengeTemplateResized
    
    def blockGrayscaleValue(self, block):
        blockWidth = block.width
        blockHeight = block.height
        blockLoad = block.load()
        blockColor = 0
        for x in range(blockWidth):
            for y in range(blockHeight):
                blockColor += blockLoad[x,y][0]

        grayscaleValue  = 1 - ((blockColor / (blockWidth * blockHeight)) / 255.0)
        # print(grayscaleValue)
        grayscaleValue = floor(grayscaleValue * self.gradientLength)
        # print(grayscaleValue)
        return self.grayscaleGradient[grayscaleValue]

    def splitToBlocks(self, grayscaleImage):
        bWidth = 7
        bHeight = 10
        resizedGrayscale = grayscaleImage.resize(((int) (grayscaleImage.width/2), (int)(grayscaleImage.height/2)), Image.ANTIALIAS)
        grayscaleWidth = resizedGrayscale.width
        grayscaleHeight = resizedGrayscale.height
        
        asciiOutput = ""
        for y in range(0, grayscaleHeight, bHeight):
            for x in range(0, grayscaleWidth, bWidth):
                blockCrop = resizedGrayscale.crop((x,y,x + bWidth,y + bHeight))
                # print(str(blockCrop.size) + " " + str(grayscaleHeight) + " " + str(grayscaleWidth))
                blockCrop = self.blockGrayscaleValue(blockCrop)
                asciiOutput += blockCrop
            asciiOutput += '\n'

        return asciiOutput

a = Image.open('1418950073149.png')
aCrop = a.crop((0,0,20,20))

aCon = asciiConverter()
aCropGray = aCon.createGrayscaleImage('1418950073149.png')
print(aCon.splitToBlocks(aCropGray))