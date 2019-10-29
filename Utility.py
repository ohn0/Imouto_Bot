from booruLib import booruLib
from gelbooruCaller import gelbooruCaller
from realbooruCaller import realbooruCaller
from sfwCaller import sfwCaller
from konachanCaller import aggregateCaller
from yandereCaller import YandereCaller

class Utility:

    def __init__(self):
        pass

    def makeRequestAndGetData(self,ctx, booruContext, arg, apiToken = None):
        caller = None

        if booruContext == booruLib.GELBOORU:
            caller = gelbooruCaller(ctx, apiToken, arg)
        elif booruContext == booruLib.REALBOORU:
            caller = realbooruCaller(ctx, booruLib.REALBOORU, arg)
        elif booruContext == booruLib.SFWBOORU:
            caller = sfwCaller(ctx, arg)
        elif booruContext == booruLib.KONACHAN:
            caller = aggregateCaller(ctx, booruLib.KONACHAN, arg)
        elif booruContext == booruLib.YANDERE:
            caller = YandereCaller(ctx,  arg)
        elif booruContext == booruLib.XBOORU:
            caller = realbooruCaller(ctx, booruLib.XBOORU, arg)
        elif booruContext == booruLib.R34:
            caller = realbooruCaller(ctx, booruLib.R34, arg)

        caller.setArgs()
        caller.makeRequest()
        return caller.getContent()

