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
from konachanCaller import KonachanCaller
from UserCollection import UserCollection
from UserStatTracker import UserStatTracker
from auditor import Auditor
from UserLimiter import UserLimiter
from timeKeeper import Timekeeper
from filter import Filter
from clientConnections import ClientConnections

configFile = open('token.config', 'r')
clientID = configFile.readline()
configFile.close()
bot = commands.Bot(command_prefix='$', case_insensitive=True)

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
async def kona(ctx, *, arg):
    if(not ctx.channel.is_nsfw()):
        await ctx.send("Can't do that on a SFW channel!")
        return False
    caller = KonachanCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
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
async def getctx(ctx):
    await ctx.send(str(ctx.guild.id) + ', ' + str(ctx.guild.name))

@bot.command(brief='gets an image from yande.re, an imageboard with highres scans. NSFW')
async def yan(ctx, *, arg):
    caller = YandereCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
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
    statMessage = "```\n--------------------------\nHere is a list of the top freaks in this channel who have made the most successful requests to this little loli!\n"
    for stat in sortedStats:
        statMessage += ("{:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))

    statMessage += "--------------------------```"
    await ctx.send(statMessage)

@bot.command(brief='gets an image from Gelbooru, an imageboard that contains a massive collection of anime images, very NSFW')
async def gel(ctx, *, arg):
    if(not ctx.channel.is_nsfw()):
        await ctx.send("Can't do that on a SFW channel!")
        return False

    if(ClientConnector.isChannelFiltered(ctx.guild.id)):
        if not ChannelFilter.isArgClean(arg.split(' ')):
            await ctx.send("Your request contained a banned tag")
            return False
    
    userLimited = True
    if(gelbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        gelbooruLimiter.limitUser(str(ctx.message.author))

    caller = gelbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
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

@bot.command(brief='It\' a traaaaap', description='Gets an image from realbooru, NSFW')
async def real(ctx, *, arg):
    userLimited = True
    if(realbooruLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        realbooruLimiter.limitUser(str(ctx.message.author))
    caller = realbooruCaller(ctx, arg)
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
    await ctx.send('This was the last request I successfully completed!'+
        '\nRequestor: {}\nfile_url: `{}`\ntags: {}'.format(lastAudit["author"], lastAudit["file_url"], lastAudit["tags"]))


@bot.command(brief='bot will disconnect')
async def bye(ctx):
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
    filterStatus = ClientConnector.toggleFilter(ctx.guild.id)
    
    if filterStatus:
        await ctx.send("Really naughty tags have been disabled for " + ctx.guild.name)
    else:
        await ctx.send("Really naughty tags have been enabled for " + ctx.guild.name + ". oh no!")

bot.run(clientID)
