import discord
from discord.ext import commands
import os
import asyncio
import random
import json
import requests
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
from clientConnections import ClientConnections
from asciiConverter import asciiConverter

configFile = open('token.config', 'r')
clientID = configFile.readline()
configFile.close()
bot = commands.Bot(command_prefix='^', case_insensitive=True)
bot.remove_command('help')

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


async def isChannelNSFW(ctx):
    isNSFW = ctx.channel.is_nsfw()
    if not isNSFW:
        await ctx.send("Can't do that on a SFW channel!")
    return isNSFW

def isExplicitlyFiltered(ctx, arg):
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        if not ChannelFilter.isArgClean(arg.split(' ')):
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

# @bot.command()
# async def 

@bot.command(brief='get uptime and startime', description='Gets the uptime and startime in UTC.')
async def uptime(ctx):
    await ctx.send("I have been working hard for {}\nI was born on {}".format(uptimeTracker.getUptime(), uptimeTracker.getStartTime()))

@bot.command(brief='uwu')
async def piss(ctx):
    await ctx.send("on me? ówò")

@bot.command(brief='why is this here', description='fuck you, hash')
async def updog(ctx):
    await ctx.send("What's up dog? " + ctx.message.author.mention)

# @bot.command()
# async def 

@bot.command(brief='bully a member')
async def bully(ctx, arg1):
    await ctx.send("{}, you're a freaky piece of trash.".format(arg1))

@bot.command()
async def bannedWords(ctx):
    print(str(ChannelFilter.getBannedWords()))

@bot.command(brief='Gets an image from konachan', description='Gets an image from konachan,an imageboard with anime wallpapers. NSFW')
@commands.check(isChannelNSFW)
async def kona(ctx, *, arg):
    extremeFiltering = False
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    caller = aggregateCaller(ctx, booruLib.KONACHAN, arg)
    caller.setArgs()
    caller.makeRequest(extremeFiltering)
    response = caller.getContent()


    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "konachan")
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")
    else:
        await ctx.send("Those tags returned no images, what's wrong with you " + ctx.message.author.mention)

@bot.command()
@commands.check(isChannelNSFW)
async def xxx(ctx, *, arg):
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
            auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "realbooru")
            await ctx.send(response["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")

        else:
            await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)

@bot.command()
@commands.check(isChannelNSFW)
async def r34(ctx, *, arg):
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
            auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "realbooru")
            await ctx.send(response["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")

        else:
            await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)
        



@bot.command(brief='gets an image from yande.re, an imageboard with highres scans. NSFW')
@commands.check(isChannelNSFW)
async def yan(ctx, *, arg):
    extremeFiltering = False
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    caller = YandereCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest(extremeFiltering)
    response = caller.getContent()

    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "yandere")
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")
    else:
        await ctx.send("Those tags returned no images, what's wrong with you " + ctx.message.author.mention)

@bot.command(brief='gets an image from safebooru, an imageboard consisting of SFW anime images.')
async def sfw(ctx, *, arg):
    caller = sfwCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    # response = caller.getResponse()

    if response != None:
        # await ctx.send("ping")
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "safebooru")
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)


@bot.command(brief='gets a list of users that have most heavily made successful requests to the bot.')
async def stats(ctx):
    currentStats = userStats.getStats()
    sortedStats = sorted(currentStats.items(), key=lambda x: x[1],reverse=True)
    statMessage = "```\n--------------------------\nI've been listening to TWICE's LIKEY too much\n"
    for stat in sortedStats:
        statMessage += ("{:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))

    statMessage += "--------------------------```"
    await ctx.send(statMessage)

@bot.command(brief='gets an image from Gelbooru, an imageboard that contains a massive collection of anime images, very NSFW')
@commands.check(isChannelNSFW)
async def gel(ctx, *, arg):
    extremeFiltering = False
    # if isExplicitlyFiltered(ctx, arg):
    #     await ctx.send("Invalid tag entered in request.")
    #     return False
        
    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        extremeFiltering = True
        if not ChannelFilter.isArgClean(arg.split(' ')):
            await ctx.send("Your request contained a banned tag")
            return False #breaks out from executing the command any further
    
    userLimited = True
    if(gelbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        gelbooruLimiter.limitUser(str(ctx.message.author))

    caller = gelbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest(extremeFiltering)
    response = caller.getContent()

    if not userLimited:
        if response != None:
            auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "gelbooru")
            await ctx.send(response["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")
        else:
            await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)

@bot.command(brief='It\'s a traaaaap', description='Gets an image from realbooru, NSFW')
@commands.check(isChannelNSFW)
async def real(ctx, *, arg):
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
            auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "realbooru")
            await ctx.send(response["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")

        else:
            await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)
        

@bot.command(brief='gets the tags for the last image posted by the bot.')
async def prev(ctx):
    lastAudit = auditor.getLastAudit()
    await ctx.send('```This was the last request I successfully completed!'+
        '\nRequestor: {}\nfile_url: `{}`\ntags: {}```'.format(lastAudit["author"], lastAudit["file_url"], lastAudit["tags"]))


@bot.command(brief='bot will disconnect')
async def bye(ctx):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You can't run that command.")
        return False
    ClientConnector.writeServerToggleStatus()
    await ctx.send("Y'all freaking me out too much, I'm out.")
    await bot.logout()
    await bot.close()

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
    



bot.run(clientID)
