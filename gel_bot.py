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
from UserCollection import UserCollection
from UserStatTracker import UserStatTracker
from sfwCaller import sfwCaller
from auditor import Auditor


clientID = 'NTI2NTA0Mzc2ODUzMDY5ODQ1.D2ScuQ.6bn-tOxaK65db0e6Cyz0ecYwPMM'
bot = commands.Bot(command_prefix='$', case_insensitive=True)

auditor = Auditor("audit.txt")
auditor.generateAuditLog()
auditLines = auditor.getInitialAuditLog()
users = UserCollection(auditLines)
userStats = UserStatTracker(users.getUsers(), auditLines)


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
    print(sortedStats)
    statMessage = "```\n-----------------------------------------------------------\nHere is a list of the top freaks in this channel who have made the most requests to this little loli!\n"
    for stat in sortedStats:
        # statMessage += (str(stat[0]) + "\t\t\t\t\t\t" + str(stat[1]) + "\n")
        statMessage += ("{:<30} {:<30}\n".format(str(stat[0]), str(stat[1])))

    statMessage += "-----------------------------------------------------------```"
    await ctx.send(statMessage)

@bot.command()
async def gel(ctx, *, arg):
    caller = gelbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    # response = caller.getResponse()

    # print(response)
    if response != None:
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        await ctx.send(response["response"])
        userStats.updateStats(str(ctx.message.author))
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)


@bot.command()
async def real(ctx, *, arg):
    caller = realbooruCaller(ctx, arg)
    caller.setArgs()
    caller.makeRequest()
    response = caller.getContent()
    # response = caller.getResponse()

    print(response)
    if response != None:
        # await ctx.send("ping")
        auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1])
        await ctx.send(response["response"])
        userStats.updateStats(str(ctx.message.author))
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    



@bot.command()
async def bye(ctx):
    await ctx.send("Y'all freaking me out too much, I'm out.")
    await bot.logout()


bot.run(clientID)

