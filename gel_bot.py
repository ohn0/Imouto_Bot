import discord
from discord.ext import commands
import os
import asyncio
import random
import json
import requests
import sys
from booruComm import booruComm
from gelbooruCaller import gelbooruCaller
from realbooruCaller import realbooruCaller
from sfwCaller import sfwCaller
from yandereCaller import YandereCaller
from konachanCaller import aggregateCaller
from UserCollection import UserCollection
from UserStatTracker import UserStatTracker
from auditor import Auditor
from UserLimiter import UserLimiter
from timeKeeper import Timekeeper
from booruLib import booruLib
from filter import Filter
import datetime
from clientConnections import ClientConnections
from asciiConverter import asciiConverter
from bullyLoader import bullyLoader
from helpResponse import helpResponse
from Utility import Utility
from ResponseProcessor import ResponseProcessor
from serverContext import ServerContext
from customFilter import CustomFilter
from customInsults import CustomInsults
from pixivComm import pixivComm

configFile = open(sys.argv[1], 'r')
clientID = configFile.readline()[0:-1]
commandPrefix = configFile.readline()[0]
pixivCredentials = {"user" : configFile.readline()[0:-1], "pw" : configFile.readline()[0:-1]}
configFile.close()
bot = commands.Bot(command_prefix=commandPrefix, case_insensitive=True)
bot.remove_command('help')
apiToken = ""
try:
    apiTokenFile = open('gelApiKey.config','r')
    apiToken = apiTokenFile.readline()
    apiTokenFile.close()
except OSError:
    print("No gelApiKey.config file found for a gelbooru api key, no api key will be used and you will not be able to access blacklisted content.")


torturing = False
auditor = Auditor("audit.txt")
auditor.generateAuditLog()
auditLines = auditor.getInitialAuditLog()
users = UserCollection(auditLines)
userStats = UserStatTracker(users.getUsers(), auditLines)
gelbooruLimiter = UserLimiter()
realbooruLimiter = UserLimiter()
uptimeTracker = Timekeeper()
ChannelFilter = Filter()
ClientConnector = ClientConnections()
bullyHandler = bullyLoader()
helpResponder = helpResponse()
responseProcessor = ResponseProcessor()
serverContextHandler = ServerContext(ClientConnector.connectedClients)
ChannelFilter.contextWordBanner = serverContextHandler
customFilterer = CustomFilter(serverContextHandler.getContext())
customInsult = CustomInsults(serverContextHandler.getContext())
auditor.populateServerInfo(serverContextHandler.getServers())

async def isChannelNSFW(ctx):
    print(ctx.channel.is_nsfw())
    isNSFW = ctx.channel.is_nsfw()
    if not isNSFW:
        await ctx.send("Can't do that on a SFW channel!")
    return isNSFW

def isExplicitlyFiltered(ctx, arg):
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        if not ChannelFilter.isArgClean(arg.split(' ')):
            return True

    if ChannelFilter.isArgCustomBanned(arg.split(' '), customFilterer.getBanContext(str(ctx.guild.id))):
        return True

    return False
    

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if len(message.mentions) == 1:
            if message.mentions[0] == bot.user:
                if 'fuck you' in message.content:
                    await message.channel.send("You're a piece of shit too.")
                elif 'sex' in message.content:
                    await message.channel.send("Be gentle okay? uwu")
                else:
                    await message.channel.send("I got summoned!")
    await bot.process_commands(message)
#      await bot.delete_message(message)


@bot.event
async def on_ready():
    print(ClientConnector.getConnectedServer())

@bot.event
async def on_guild_join(guild):
    ClientConnector.updateConnectedClients(guild.id)
    auditor.insertNewContext(str(guild.id))
    customFilterer.insertNewContext(str(guild.id))
    customInsult.insertNewContext(str(guild.id))


# @bot.command()
# async def 

@bot.command(brief='get uptime and startime', description='Gets the uptime and startime in UTC.')
async def uptime(ctx):
    await ctx.send("I have been working hard for {}\nI was born on {}".format(uptimeTracker.getUptime(), uptimeTracker.getStartTime()))

@bot.command(brief='uwu')
async def piss(ctx, arg = None):
    if arg is None:
        await ctx.send("on me? ówò")
    else:
        if ctx.channel.is_nsfw():
            pissImage = open('tasty.gif', 'rb')
            await ctx.send("okay papi I'll squirt my love liquid onto  {}".format(arg), file = discord.File(pissImage))
        else:
            pissImage = open('turtlepiss.gif', 'rb')
            await ctx.send("okay papi I'll squirt my love liquid onto  {}".format(arg), file = discord.File(pissImage))


@bot.command(brief='why is this here', description='fuck you, hash')
async def updog(ctx):
    await ctx.send("What's up dog? " + ctx.message.author.mention)


@bot.command(brief='bully a member')
async def bully(ctx, arg1):
    await ctx.send("{}, I'ma fucking rape you with a plunger tonight bby".format(arg1))

@bot.command()
async def bannedWords(ctx):
    print(str(ChannelFilter.getBannedWords()))

@bot.command()
async def eatmycum(ctx):
    await ctx.send("**_I'M HUNGRY_**")

@bot.command(brief='Gets an image from konachan', description='Gets an image from konachan,an imageboard with anime wallpapers. NSFW')
@commands.check(isChannelNSFW)
async def kona(ctx, *, arg):
    await keyKona(ctx, arg)

async def keyKona(ctx, arg):
    extremeFiltering = False
    arg += generateCustomBanList(str(ctx.guild.id))
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')) or ChannelFilter.isArgCustomBanned(arg.split(' '), customFilterer.getBanContext(str(ctx.guild.id))):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    caller = aggregateCaller(ctx, booruLib.KONACHAN, arg)
    caller.setArgs()
    caller.makeRequest(extremeFiltering)
    response = caller.getContent()
    if response != None:
        await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
    else:
        await noImageFoundHandler(ctx)

@bot.command()
@commands.check(isChannelNSFW)
async def xxx(ctx, *, arg):
    await keyXxx(ctx, arg)

async def keyXxx(ctx, arg):
    arg += generateCustomBanList(str(ctx.guild.id))
    if isExplicitlyFiltered(ctx, arg):
        await ctx.send("Invalid tag entered in request.")
        return False
    userLimited = True
    if(realbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        realbooruLimiter.limitUser(str(ctx.message.author))
    caller = realbooruCaller(ctx, booruLib.XBOORU ,arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    if not userLimited:
        if response != None:
            await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
        else:
            await noImageFoundHandler(ctx)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)

@bot.command()
@commands.check(isChannelNSFW)
async def r34(ctx, *, arg):
    await invoker34(ctx, arg)
        

async def invoker34(ctx, arg):
    arg += generateCustomBanList(str(ctx.guild.id))
    if isExplicitlyFiltered(ctx, arg):
        await ctx.send("Invalid tag entered in request.")
        return False
    userLimited = True
    if(realbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        realbooruLimiter.limitUser(str(ctx.message.author))
    caller = realbooruCaller(ctx, booruLib.R34 ,arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    if not userLimited:
        if response != None:
            await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
        else:
            await noImageFoundHandler(ctx)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)



@bot.command(brief='gets an image from yande.re, an imageboard with highres scans. NSFW')
@commands.check(isChannelNSFW)
async def yan(ctx, *, arg):
    await keyYan(ctx,arg)

async def keyYan(ctx, arg):
    arg += generateCustomBanList(str(ctx.guild.id))    
    extremeFiltering = False
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')) or ChannelFilter.isArgCustomBanned(arg.split(' '), customFilterer.getBanContext(str(ctx.guild.id))):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    caller = YandereCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest(extremeFiltering)
    response = caller.getContent()

    if response != None:
        await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
    else:
        await noImageFoundHandler(ctx)
        # await ctx.send("Those tags returned no images, what's wrong with you " + ctx.message.author.mention)

@bot.command(brief='gets an image from safebooru, an imageboard consisting of SFW anime images.')
async def sfw(ctx, *, arg):
    await keySfw(ctx, arg)

async def keySfw(ctx, arg):
    arg += generateCustomBanList(str(ctx.guild.id))    
    caller = sfwCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()

    if response != None:
        await responseProcessor.interpretResponse(auditor, ctx, response, userStats)

    else:
        await noImageFoundHandler(ctx)


@bot.command(brief='gets a list of users that have most heavily made successful requests to the bot.')
async def stats(ctx):
    currentStats = userStats.getStats()
    sortedStats = sorted(currentStats.items(), key=lambda x: x[1],reverse=True)
    statMessage = "```\n\nHow can you make a loli do this\n```"
    await ctx.send(statMessage)
    messages = []
    counter = 0
    statCounter = 0
    messages.append("```")
    for stat in sortedStats:
        statCounter+=1
        messages[counter] += (str(statCounter) + " {:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))
        if statCounter % 10 == 0:
            messages[counter] += "```"
            counter+=1
            messages.append("```")
    
    messages[counter] += "```"
    
    for message in messages:
        print(message)
        await ctx.send(message)

@bot.command(brief='gets an image from Gelbooru, an imageboard that contains a massive collection of anime images, very NSFW')
@commands.check(isChannelNSFW)
async def gel(ctx, *, arg):
    await keyGel(ctx, arg) 

async def keyGel(ctx, arg):
    arg = arg +  generateCustomBanList(str(ctx.guild.id))
    extremeFiltering = False
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')) or ChannelFilter.isArgCustomBanned(arg.split(' '), customFilterer.getBanContext(str(ctx.guild.id))):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    
    userLimited = True
    if(gelbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        gelbooruLimiter.limitUser(str(ctx.message.author))


    if not userLimited:
        caller = gelbooruCaller(ctx, apiToken, arg)
        caller.setArgs()
        caller.makeRequest(extremeFiltering)
        response = caller.getContent()

        if response != None:
            await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
        else:
            await noImageFoundHandler(ctx)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)

@bot.command(brief='It\'s a traaaaap', description='Gets an image from realbooru, NSFW')
@commands.check(isChannelNSFW)
async def real(ctx, *, arg):
    await keyReal(ctx, arg)

async def keyReal(ctx, arg):
    arg += generateCustomBanList(str(ctx.guild.id))
    if isExplicitlyFiltered(ctx, arg):
        await ctx.send("Invalid tag entered in request.")
        return False
    userLimited = True
    if(realbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        realbooruLimiter.limitUser(str(ctx.message.author))
    caller = realbooruCaller(ctx, booruLib.REALBOORU ,arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    if not userLimited:
        if response != None:
            await responseProcessor.interpretResponse(auditor, ctx, response, userStats)
        else:
            await noImageFoundHandler(ctx)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)
        

@bot.command(brief='gets the tags for the last image posted by the bot.')
async def prev(ctx):
    lastAudit = auditor.getLastAudit(str(ctx.guild.id))
    await ctx.send('```This was the last request I successfully completed!'+
        '\nRequestor: {}\nfile_url: `{}`\ntags: {}```'.format(lastAudit["author"], lastAudit["file_url"], lastAudit["tags"]))


@bot.command(brief='bot will disconnect')
async def bye(ctx):
    if(int(ctx.author.id) == 452972260547100692):
        await ctx.send("Y'all freaking me out too much, I'm out.")
        customFilterer.saveContexts(serverContextHandler)
        customInsult.saveContexts(serverContextHandler)
        serverContextHandler.writeContextsToFile()
        ClientConnector.writeServerToggleStatus()
        await bot.logout()
        await bot.close()
    else:
        await ctx.send("You can't run that command.")
        return False

@bot.command(brief='unused atm')
async def tagStats(ctx):
    print(ctx.message.content) 


@bot.command(brief='prints a gem')
async def gem(ctx):
    await ctx.send(":gem:")

@bot.command(brief='turns on the ChannelFilter')
async def toggleFilter(ctx):


    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False

    filterStatus = ClientConnector.toggleFilter(ctx.guild.id)
    
    if filterStatus:
        await ctx.send("Really naughty tags have been disabled for " + ctx.guild.name)
    else:
        await ctx.send("Really naughty tags have been enabled for " + ctx.guild.name + ". oh no!")


@bot.command(brief='Info about bot and usage.')
async def about(ctx):
    await ctx.send("Here's a github with more info about myself!\nhttps://github.com/ohn0/Imouto_Bot")
    await ctx.send('''
^gel <arg1> <arg2> <arg3>
^kona <arg1> ...
^yan  <arg1> ...
^sfw  <arg1> ...
^real <arg1> ...
if the arg is multiple words, replace spaces with '_'
ex: 'black lagoon' -> black_lagoon
can add multiple tags separated by space
ex: ^gel azur_lane swimsuit beach
^gel searches gelbooru,  hentai pics
^kona searches konachan, anime wallpapers
^yan searches yande.re,  highres images and artbook scans
^sfw searches safebooru, SFW anime images
^real searches realbooru, traps galore 
''')

@bot.command(brief='send an image file.')
async def send(ctx):
    try:
        #await ctx.send("lol fuck you, I'm not saving shit anymore you freak {}".format(ctx.message.author.mention))
        bytesSaved = await ctx.message.attachments[0].save(ctx.message.attachments[0].filename)
        AsciiConverter = asciiConverter()
        grayImage = AsciiConverter.createGrayscaleFile(ctx.message.attachments[0].filename)
        #TODO: show message that save was completed.
        if bytesSaved > 0:
            grayscaleImg = open(grayImage,'rb')
            await ctx.send("Here you go, bitch, {}".format(ctx.message.author.mention), file=discord.File(grayscaleImg))
    except discord.NotFound:
        await ctx.send("File was deleted before I could save it!")
    except discord.HTTPException:
        await ctx.send("Saving the file failed.")

@bot.command()
async def avenge(ctx):
    try:
        #await ctx.send("lol fuck you, I'm not saving shit anymore you freak {}".format(ctx.message.author.mention))
        bytesSaved = await ctx.message.attachments[0].save(ctx.message.attachments[0].filename)
        AsciiConverter = asciiConverter()
        grayImage = AsciiConverter.applyAvengerTemplate(ctx.message.attachments[0].filename)
        #TODO: show message that save was completed.                
        if bytesSaved > 0:
            grayscaleImg = open(grayImage,'rb')
            await ctx.send("Here you go, bitch, {}".format(ctx.message.author.mention), file=discord.File(grayscaleImg))
    except discord.NotFound:
        await ctx.send("File was deleted before I could save it!")
    except discord.HTTPException:
        await ctx.send("Saving the file failed.")


@bot.command()
async def art(ctx):
    bytesSaved = await ctx.message.attachments[0].save(ctx.message.attachments[0].filename)
    AsciiConverter = asciiConverter()
    blockString = AsciiConverter.splitToBlocks(AsciiConverter.createGrayscaleImage(ctx.message.attachments[0].filename))
    print(blockString)
    await ctx.send(blockString)    


@bot.command()
async def banW(ctx, *, arg):

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False
    else:
        if customFilterer.banWordContext(str.lower(arg), str(ctx.guild.id)):
            await ctx.send(arg + " was banned!")
        else:
            await ctx.send(arg + " is already banned!")

@bot.command()
async def unbanW(ctx, *, arg):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False
    else:
        if customFilterer.unbanWordContext(str.lower(arg), str(ctx.guild.id)):
            await ctx.send(arg + " was unbanned!")
        else:
            await ctx.send(arg + " was never banned!")

@bot.command()
async def help(ctx, arg = None):
    if arg == None or arg not in Utility.helpOptions:
        helpImage = helpResponder.getResponseImage()
        await ctx.send("Help incoming!", file=discord.File('.//responses//'+ helpImage))
        await ctx.send("Type ^help search/admin/insult/misc to get more help about the specific topic(searching, insults, admin, misc).")
    else:
        await ctx.send(Utility.helpOptions[arg])

#     await ctx.send('''
# ^gel <arg1> <arg2> <arg3>
# ^kona <arg1> ...
# ^yan  <arg1> ...
# ^sfw  <arg1> ...
# ^real <arg1> ...
# if the arg is multiple words, replace spaces with '_'
# ex: 'black lagoon' -> black_lagoon
# can add multiple tags separated by space
# ex: ^gel azur_lane swimsuit beach
# ^gel searches gelbooru,  hentai pics
# ^kona searches konachan, anime wallpapers
# ^yan searches yande.re,  highres images and artbook scans
# ^sfw searches safebooru, SFW anime images
# ^real searches realbooru, traps galore,
# ^r34 searches rule34booru, find porn of anything you want except yourself because even you're not that wanted
# ----
# You can search for tags faster by adding %% to the request
# ----
# You can search for multiple images at once by appending '--numbX' after the tags, with X replacing however many images you want capped at 9 
# ex: ^gel cake --numb3 -> results in 3 images that have cake in them being posted
# ----
# ^rand <gel|kona|yan|sfw|real|r34|xxx> returns a random image from the specified source
# ---
# You can add and remove insults for the  server to use
# ^addinsult <insult> adds the insult
# ^removeinsult <insult key> removes the insult, you need to specify the number of the insult that is returned when you use ^insultlist
# ^insultlist returns a list of insults along with a numbered key to access them for deletion
# ---
# You can ban specific words across your server
# ^banw <word> prevents any request from succeeding if <word> is in the request
# ^unbanw <word> allows requests with <word> if it was previously banned
# ^banlist returns a list of all banned words on the server
# ''')


async def noImageFoundHandler(ctxVal, arg1 = None):
    # insult = bullyHandler.getInsult()
    insult = customInsult.getInsultContext(str(ctxVal.guild.id))

    if serverContextHandler.getContextConfigKeyValue(str(ctxVal.guild.id),"disgust"):
        insultIndex = random.randint(0, len(insult))
    else:
        insultIndex = random.randint(0, len(insult)-1)    

    if(insultIndex == len(insult)):
        if arg1 != None:
            await ctxVal.send("{}".format(arg1), file=discord.File('.//responses//disgusting.png'))
        else:
            await ctxVal.send("{}".format(ctxVal.message.author.mention), file=discord.File('.//responses//disgusting.png'))
    else:
        if arg1 != None:
            await ctxVal.send("{}, {}".format(arg1, insult[insultIndex]))
        else:
            await ctxVal.send("{}, {}".format(ctxVal.message.author.mention, insult[insultIndex]))


@bot.command()
async def banList(ctx):
    bannedWordList = customFilterer.getBanContext(str(ctx.guild.id))
    words = "```\n"
    for word in bannedWordList:
        words += word + "\n"
    words += "```"
    await ctx.send("These are the banned words on this server:\n" + words)

@bot.command()
async def top10(ctx):
    currentStats = userStats.getStats()
    sortedStats = sorted(currentStats.items(), key=lambda x: x[1],reverse=True)
    statMessage = "```\n\nThese are the top 10 people who abuse this loli the most\n```"
    await ctx.send(statMessage)
    messages = []
    counter = 0
    statCounter = 0
    messages.append("```")
    while statCounter < 10:
        # statMessage += ("{:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))
        messages[counter] += (str(statCounter+1) + " {:<30} {:<30}\n".format(str(sortedStats[statCounter][0]), str(sortedStats[statCounter][1])))
        statCounter+=1
    messages[counter] += "```"
    
    for message in messages:
        print(message)
        await ctx.send(message)


@bot.command()
async def insult(ctx, arg1):
    await noImageFoundHandler(ctx, arg1)

@bot.command()
async def addInsult(ctx, *, arg):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False
    else:
        customInsult.addInsultContext(arg, str(ctx.guild.id))
        await ctx.send("I learned a new insult! >:D\n"+ arg)

@bot.command()
async def removeInsult(ctx, *, arg):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False
    else:
        success = False
        try:
            success = customInsult.deleteInsultContext(int(arg[0]) - 1, str(ctx.guild.id))
        except ValueError:
            success = False

        if not success:
            await ctx.send("I can't find that insult for this server. type ^insultlist to get a list and send me the number of the insult I need to remove.")
        else:
            await ctx.send("I forgot an insult!")

@bot.command()
async def insultlist(ctx):
    customInsults = customInsult.getInsultContext(str(ctx.guild.id))
    insults = "```\n"
    counter = 1
    for insult in customInsults:
        insults += str(counter) + ". " + insult + "\n"
        counter+=1
    insults += "```"
    await ctx.send("these are all the insults I know on this server.\n" + insults)

@bot.command()
async def toggleDisgust(ctx):

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
    else:
            
        updatedValue = serverContextHandler.toggleContextConfig(str(ctx.guild.id),"disgust")

        if updatedValue:
            await ctx.send("disgust image will be used in insults")
        else:
            await ctx.send("disgust image will not be used in insults")

@bot.command()
async def togglePiss(ctx):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
    else:
        updateValue = serverContextHandler.toggleContextConfig(str(ctx.guild.id), "piss")
        
        if updateValue:
            await ctx.send("piss image will be used")
        else:
            await ctx.send("piss image will not be used.")

@bot.command()
async def toggleLoli(ctx):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
    else:
        updateValue = serverContextHandler.toggleContextConfig(str(ctx.guild.id), "loli")

        if updateValue:
            await ctx.send("lolibooru can now be used. Nevermind lolibooru doesn't exist anymore.")
        else:
            await ctx.send("lolibooru can no longer be used.")

@bot.command()
async def rand(ctx, *, arg):
    source = arg
    pid = "&pid="+str(random.randint(0, 100))
    if source == "gel":
        await keyGel(ctx,arg = "* "+pid)
    elif source == "yan":
        await keyYan(ctx,arg = "* "+pid)
    elif source == "kona":
        await keyKona(ctx,arg = "* "+pid)
    elif source == "sfw":
        await keySfw(ctx,arg = "* "+pid)
    elif source == "real":
        await keyReal(ctx,arg = "* "+pid)
    elif source == "r34":
        await invoker34(ctx,arg = "* "+pid)
    elif source == "xxx":
        await keyXxx(ctx,arg = "* "+pid)
    else:
        await ctx.send("Invalid source entered. only the following are valid sources:\ngel\nyan\nkona\nsfw\nreal\nr34\nxxx")

def generateCustomBanList(guildID):
    customBans =  customFilterer.getBanContext(guildID)
    customBanArgs = " "
    for ban in customBans:
        customBanArgs += "-{} ".format(ban)
    return customBanArgs

@bot.command()
async def lovefeet(ctx):
    try:
        #await ctx.send("lol fuck you, I'm not saving shit anymore you freak {}".format(ctx.message.author.mention))
        bytesSaved = await ctx.message.attachments[0].save(ctx.message.attachments[0].filename)
        AsciiConverter = asciiConverter()
        AsciiConverter.loveFeet(ctx.message.attachments[0].filename)
        #TODO: show message that save was completed.                
        if bytesSaved > 0:
            grayscaleImg = open('ratCopy.png','rb')
            await ctx.send("Here you go, bitch, {}".format(ctx.message.author.mention), file=discord.File(grayscaleImg))
    except discord.NotFound:
        await ctx.send("File was deleted before I could save it!")
    except discord.HTTPException:
        await ctx.send("Saving the file failed.")


@bot.command()
async def corona(ctx):
    coronaResponse = requests.get('https://api.covid19api.com/summary').json()
    coronaStatus = str(coronaResponse['Global']['TotalDeaths']) + " people have died due to corona!\n" + str(coronaResponse['Global']['TotalConfirmed']) + " people have been confirmed to have coronavirus!\n" + str(coronaResponse['Global']['TotalRecovered']) + " have recovered from coronavirus!\n"
    await ctx.send(coronaStatus)


@bot.command()
async def recovered(ctx):
    coronaResponse = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest').json()
    await ctx.send(str(coronaResponse['latest']['recovered']) + " people have recovered from corona!")

@bot.command()
async def diagnosed(ctx):
    coronaResponse = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest').json()
    await ctx.send(str(coronaResponse['latest']['confirmed']) + " people currently have corona!")


@bot.command()
async def rule6(ctx):
    await ctx.send("Mantieni la chat in inglese (principalmente). Questo è un server di lingua inglese. Cerca di mantenere le conversazioni in inglese se non assolutamente necessario.")    
    
@bot.command()
async def pixiv(ctx, *, args):
    pixivCall = pixivComm(pixivCredentials)
    foundImage = pixivCall.searchImage(args)
    await ctx.send("Here you go! ", file=discord.File(open(foundImage, 'rb')))


bot.run(clientID)
