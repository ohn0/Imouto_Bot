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

configFile = open('token.config', 'r')
clientID = configFile.readline()
configFile.close()
bot = commands.Bot(command_prefix='$', case_insensitive=True)

auditor = Auditor("audit.txt")
auditor.generateAuditLog()
auditLines = auditor.getInitialAuditLog()
users = UserCollection(auditLines)
userStats = UserStatTracker(users.getUsers(), auditLines)
userLimiter = UserLimiter()

@bot.command()
async def bully(ctx, arg1):
    await ctx.send("{}, you're a freaky piece of trash.".format(arg1))

@bot.command()
async def kona(ctx, *, arg):
    caller = KonachanCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()

    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])
    else:
        await ctx.send("Those tags returned no images, what's wrong with you " + ctx.message.author.mention)

@bot.command()
async def yan(ctx, *, arg):
    caller = YandereCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()

    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])
    else:
        await ctx.send("Those tags returned no images, what's wrong with you " + ctx.message.author.mention)

@bot.command()
async def sfw(ctx, *, arg):
    caller = sfwCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    # response = caller.getResponse()

    if response != None:
        # await ctx.send("ping")
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        userStats.updateStats(str(ctx.message.author))
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)


@bot.command()
async def stats(ctx):
    currentStats = userStats.getStats()
    sortedStats = sorted(currentStats.items(), key=lambda x: x[1],reverse=True)
    statMessage = "```\n--------------------------\nHere is a list of the top freaks in this channel who have made the most successful requests to this little loli!\n"
    for stat in sortedStats:
        statMessage += ("{:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))

    statMessage += "--------------------------```"
    await ctx.send(statMessage)

@bot.command()
async def gel(ctx, *, arg):
    userLimited = True
    if(userLimiter.checkIfLimited(str(ctx.message.author)) == False):
        userLimited = False
        userLimiter.limitUser(str(ctx.message.author))

    caller = gelbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()

    if not userLimited:
        if response != None:
            auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
            await ctx.send(response["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n" + response["tags"])
        else:
            await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    else:
        await ctx.send("You just made a request! Your little sister can only do so much uwu " + ctx.message.author.mention)

@bot.command()
async def real(ctx, *, arg):
    caller = realbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()

    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        await ctx.send(response["response"])
        userStats.updateStats(str(ctx.message.author))
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    

@bot.command()
async def prev(ctx):
    lastAudit = auditor.getLastAudit()
    await ctx.send('This was the last request I successfully completed!'+
        '\nRequestor: {}\nfile_url: `{}`\ntags: {}'.format(lastAudit["author"], lastAudit["file_url"], lastAudit["tags"]))


@bot.command()
async def bye(ctx):
    await ctx.send("Y'all freaking me out too much, I'm out.")
    await bot.logout()

@bot.command()
async def tagStats(ctx):
    print(ctx.message.content)


bot.run(clientID)

