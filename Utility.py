from booruLib import booruLib
from gelbooruCaller import gelbooruCaller
from realbooruCaller import realbooruCaller
from sfwCaller import sfwCaller
from konachanCaller import aggregateCaller
from yandereCaller import YandereCaller

class Utility:



    searchHelp = '''
^gel <arg1> <arg2> <arg3>
^kona <arg1> ...
^yan  <arg1> ...
^sfw  <arg1> ...
^real <arg1> ...
^r34 <arg1> ...
^xxx <arg1>
if the arg is multiple words, replace spaces with '_'
ex: 'black lagoon' -> black_lagoon
You can add multiple tags separated by space to look up specific images
ex: ^gel azur_lane swimsuit beach
^gel searches gelbooru,  hentai pics
^kona searches konachan, anime wallpapers
^yan searches yande.re,  highres images and artbook scans
^sfw searches safebooru, SFW anime images
^real searches realbooru, traps galore,
^r34 searches rule34booru, find porn of anything you want except yourself because even you're not that wanted
----
You can search for tags faster by adding %% to the request, this will return the image along with all the tags that are used in that image.
----
You can search for multiple images at once by appending '--numbX' after the tags, with X replacing however many images you want capped at 9 
ex: ^gel cake --numb3 -> results in 3 images that have cake in them being posted
----
^rand <gel|kona|yan|sfw|real|r34|xxx> returns a random image from the specified source, this does not take any tags so it can return any random image.
^prev returns the tags of the last image posted
'''

    insultHelp = '''
You can add and remove insults for the  server to use
^insultlist returns a list of insults along with a numbered key to access them for deletion
^addinsult <insult> adds the insult
^removeinsult <insult key> removes the insult, you need to specify the number of the insult that is returned when you use ^insultlist
^insult <user> will send an insult to the specified user pulling an insult from the list of insults that are in the server.
'''

    adminHelp = '''
You can ban specific words across your server
^banw <word> prevents any request from succeeding if <word> is in the request
^unbanw <word> allows requests with <word> if it was previously banned
^banlist returns a list of all banned words on the server
^togglefilter toggles whether global banned words can be used on this server or not.
'''

    miscHelp = '''
^stats returns the global list of users who have requested the most images from the bot
^top10 returns a top10 list of people who have abused the bot the most.
^piss pissed on the bot or on a specified user if they are specified.
^updog ???
'''

    helpOptions = {
        'search' : searchHelp,
        'insult' : insultHelp,
        'misc' : miscHelp,
        'admin' : adminHelp
    }

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

