class ResponseProcessor:

    def __init__(self):
        pass

    async def interpretResponse(self, auditor, ctx, response, userStats):
        for i in range(response["values"]):
            auditor.audit(str(ctx.message.author), response["auditMessage"][i]["message"], response["auditMessage"][i]["tags"])
            # auditor.audit(str(ctx.message.author), response["auditMessage"][0], response["auditMessage"][1], "gelbooru")
            await ctx.send(response["auditMessage"][i]["response"])
            userStats.updateStats(str(ctx.message.author))
            if(response["sendTags"]):
                await ctx.send("These are the tags I found with that image: \n```" + response["tags"]+"```\n")