@bot.command()
async def gel(ctx, *, arg):
    #GelCaller = gelbooruComm()
    #GelCaller.setArgs(arg)
    #GelCaller.makeRequest()
    sendTags = False
    print(arg.split(" "))
    argList = arg.split(" ")
    randPost = random.randint(0, 50)
    tagList = ""
    responseMessage = ctx.message.author.mention + ", I got an image for you. "
    params = []
    imageReturned = True
    for arg in argList:
        if(not arg.startswith('--')):
            tagList = arg + "+"+ tagList
        else:
            params.append(arg)

    for param in params:
        if param == '--tags':
            sendTags = True

    tagList = tagList[0:len(tagList)-1]

    apicall = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit="+str(randPost)+"&json=1&tags="+tagList
    try:
        response = requests.get(apicall)
        response = response.json()
    except json.decoder.JSONDecodeError:
        imageReturned = False

    if imageReturned:
        imageNum = random.randint(0, randPost -1)
        responseMessage += response[imageNum]['file_url']
        auditor.audit(str(ctx.message.author), str(response[imageNum]['file_url']), str(response[imageNum]['tags']))
        await ctx.send(responseMessage)
        if sendTags:
            await ctx.send("These are the tags associated with the image I just posted: \r" + response[imageNum]['tags'])
    else: 
        await ctx.send("Those tags returned no images, try again, you freak, " + ctx.message.author.mention)
