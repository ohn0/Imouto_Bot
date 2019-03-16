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
from auditor import Auditor


clientID = 'NTI2NTA0Mzc2ODUzMDY5ODQ1.D2ScuQ.6bn-tOxaK65db0e6Cyz0ecYwPMM'
client = discord.Client()
bot = commands.Bot(command_prefix='$', case_insensitive=True)


auditor = Auditor("audit.txt")

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
        await ctx.send(response["response"])
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)


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
        if(response["sendTags"]):
            await ctx.send("These are the tags I found with that image: \n" + response["tags"])

    else:
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
    



@bot.command()
async def bye(ctx):
    await ctx.send("Y'all freaking me out too much, I'm out.")
    await bot.close()



bot.run(clientID)
auditor.closeFile()

