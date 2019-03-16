import discord
from discord.ext import commands
import os
import asyncio
import random
import requests

client = discord.Client()
bot = commands.Bot(command_prefix='$', case_insensitive=True)
loggedIn = False
imgFiles = os.listdir('D:\\[a] pics')
imgDirLen = len(imgFiles)

webmFiles = os.listdir('C:\\Users\\Neel\\Downloads\\webmN')
webmDirLen = len(webmFiles)


weebpics = 'D:\\weebpics\\weeb'
sfwpics = 'C:\\Users\\Neel\\Pictures'
npics = 'C:\\Users\\Neel\\anime\\Jessica Nigri Photos March.August 2018\\JN\\collection'
apoloniaPics = "D:\\BLACKED - HQ PICTURES - Apolonia Lapiedra - Spring Break BBC"
wtfPics = "D:\\Anime\\JAV & H\\H stuff\\hentai\\[120824][Vanadis] Sei Monmusu Gakuen CG"
anriPics = "C:\\Users\\Neel\\discord_bots\\content\\AnriMarieFull\\anrimarie01"
darkPics = "C:\\Users\\Neel\\discord_bots\\content\\dark\\Dark elf girl mix (classic, night elf, drow, danmer, Dark elf, Korra)"
ahePics = "C:\\Users\\Neel\discord_bots\\content\\AhegaoColl"
cosplayPics = "C:\\Users\\Neel\\discord_bots\\content\\nikumikyo"

sfwFiles = os.listdir(sfwpics)
sfwDirLen = len(sfwFiles)

aheFiles = os.listdir(ahePics)
aheDirLen = len(aheFiles)

cosplayFiles = os.listdir(cosplayPics)
cosplayDirLen = len(cosplayFiles)

aiFiles = os.listdir('C:\\Users\\Neel\\Downloads\\Ai Uehara - Imgur')
aiDirLen = len(aiFiles)

juliaFiles = os.listdir('C:\\Users\\Neel\\Downloads\\Julia - Imgur')
juliaDirLen = len(juliaFiles)

apoloniaFiles = os.listdir(apoloniaPics)
apoloniaDirLen = len(apoloniaFiles)

nFiles = os.listdir(npics)
nDirLen = len(nFiles)

wtfFiles = os.listdir(wtfPics)
wtfDirLen = len(wtfFiles)

anriFiles = os.listdir(anriPics)
anriDirLen = len(anriFiles)

darkFiles = os.listdir(darkPics)
darkDirLen = len(darkFiles)

'''gianna dior
melanie iglesias
apolonia lapiedra
yanet garcia
alina lopez
janet guzman'''

def getRandImage():
    return imgFiles[random.randint(0,imgDirLen)]

def getRandNSFWWEBM():
    return webmFiles[random.randint(0, webmDirLen)]

def getRandSFW():
    return sfwFiles[random.randint(0, sfwDirLen)]

def getAi():
    return aiFiles[random.randint(0, aiDirLen-1)]

def getJULIA():
    return juliaFiles[random.randint(0, juliaDirLen-1)]

def getApolonia():
    return apoloniaFiles[random.randint(0, apoloniaDirLen-1)]

def getNpics():
    return nFiles[random.randint(0, nDirLen-1)]

def getWtf():
    return wtfFiles[random.randint(0, wtfDirLen-1)]

def getAnri():
    return anriFiles[random.randint(0, anriDirLen-1)]

def getDark():
    return darkFiles[random.randint(0, darkDirLen-1)]

def  getAhegao():
    return aheFiles[random.randint(0, aheDirLen-1)]

def getCosplay():
    return cosplayFiles[random.randint(0, cosplayDirLen-1)]

@bot.command()
async def hello(ctx):
    await ctx.send(ctx.message.author.mention + ', what the fuck do you want?')

@bot.command()
async def anri(ctx):
        await ctx.send(ctx.message.author.mention + ", Here's an anri image", file=discord.File(anriPics + "\\" + getAnri()))

@bot.command()
async def ahegao(ctx):
        await ctx.send(ctx.message.author.mention + ", Here's some ahegao image", file=discord.File(ahePics + "\\" + getAhegao()))

@bot.command()
async def randomImg(ctx):
    await ctx.send(ctx.message.author.mention + ", Here's a random image from 'D:\\[a] pics, MIGHT BE NSFW!", file=discord.File('D:\\[a] pics\\'+getRandImage()))

@bot.command()
async def nigri(ctx):
    await ctx.send(ctx.message.author.mention + ", Here's something:", file=discord.File(npics+ '\\' +getNpics()))

@bot.command()
async def gel(ctx,*, arg):
    print(arg.split(" "))
    argList = arg.split(" ")
    randPage = random.randint(0, 5)
    randPost = random.randint(0, 50)
    tagList = ""
    for a in argList:
        tagList = a + "+" + tagList
    tagList = tagList[0:len(tagList)-1]
    # apicall = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&pid="+str(randPage)+"&limit="+str(randPost)+"&json=1&tags="+tagList
    apicall = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit="+str(randPost)+"&json=1&tags="+tagList

    response = requests.get(apicall)
    response = response.json()
    await ctx.send(ctx.message.author.mention + ", here you go: " + response[random.randint(0,randPost-1)]['file_url'])

@bot.command()
async def wtf(ctx):
    await ctx.send(ctx.message.author.mention + ", Here's something:", file=discord.File(wtfPics+ '\\' +getWtf()))

@bot.command()
async def dark(ctx):
    await ctx.send(ctx.message.author.mention + ", Here's something:", file=discord.File(darkPics+ '\\' +getDark()))

@bot.command()
async def cosplay(ctx):
    await ctx.send(ctx.message.author.mention + ", Here's something:", file=discord.File(cosplayPics+ '\\' +getCosplay()))


@bot.command()
async def bullyHash(ctx):
    await ctx.send("Hash a big scrub")

@bot.command()
async def bully(ctx, arg):
    insults = ['is a chinky e-thot',
               'is a loli loving freak',
               'is a tiny dicked retard',
               'is a cart master',
               'is a shitty south asian',
               'is a kimchi cowfucker',
                'is an orphan',
                'likes traps',
                'really wants to fuck a train',
                'is a trap pornstar',
                'gets turned on by hobos blowing other hobos'
                ]

    await ctx.send(arg + ' ' + insults[random.randint(0, len(insults)-1)])

@bot.command()
async def bitch(ctx):
    await ctx.send("Hash, you're a fucking bitch")

@bot.command()
async def ai(ctx):
    await ctx.send("Here's an Ai pic " + ctx.message.author.mention, file=discord.File("C:\\Users\\Neel\\Downloads\\Ai Uehara - Imgur\\"+getAi()))

@bot.command()
async def julia(ctx):
    await ctx.send("Here's a Julia pic " + ctx.message.author.mention, file=discord.File("C:\\Users\\Neel\\Downloads\\Julia - Imgur\\"+getJULIA()))

@bot.command()
async def nsfw(ctx):
    await ctx.send("Incoming NSFW requested by " + ctx.message.author.mention +". You're a fucking disgusting freak for requesting this.", file=discord.File('C:\\Users\\Neel\\Downloads\\webmN\\'+getRandNSFWWEBM()))    

@bot.command()
async def sfw(ctx):
    await ctx.send("Incoming SFW requested by " + ctx.message.author.mention, file=discord.File(sfwpics+ '\\' +getRandSFW()))

@bot.command()
async def latina(ctx):
    await ctx.send("Here's a latina " + ctx.message.author.mention, file=discord.File(apoloniaPics + "\\" + getApolonia()))


@bot.command()
async def bye(ctx):
    await ctx.send("bye!")
    await bot.close()

@bot.command()
async def hentai(ctx):
    await ctx.send("Incoming NSFW requested by " + ctx.message.author.mention, file=discord.File('image.jpg'))    

@bot.command()
async def loli(ctx):
    await ctx.send("Incomoing loli requested by " + ctx.message.author.mention, file=discord.File('ilya.png'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    returnedMessage = message.content
    print(returnedMessage)

    if message.content.startswith('garbage'): #or message.content.startswith('Garbage'):
        await bot.send(message.author.mention + ", You're the piece of garbage, scrub.")

    #await message.channel.send('You posted a message ' + message.author.mention)
    print('processing an event')
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("I live!")
    # if not loggedIn:
    #     loggedIn = True
    #     # await 

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(ctx.message.author.mention +  "That command does not exist.")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # message.channel.send('{0.user} has logged into the server!'.format(client));


@client.event
async def on_connect():
    print('Client has successfully connected to Discord! Yay!');


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await  message.channel.send('Hello! ' + message.author.name + ', you\'re a bitch!.')
        

    if message.content.startswith('send'):
        #channel = client.get_channel(553733457100931085)
        await client.send('1234')

    if message.content.startswith('close'):
        print('ffs')




bot.run('NTI2NTA0Mzc2ODUzMDY5ODQ1.D2ScuQ.6bn-tOxaK65db0e6Cyz0ecYwPMM')
# client.run('NTI2NTA0Mzc2ODUzMDY5ODQ1.D2ScuQ.6bn-tOxaK65db0e6Cyz0ecYwPMM')