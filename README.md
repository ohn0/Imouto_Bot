Test server:
https://discord.gg/2Eytgk3
Come mess around with the bot!

Invite the bot to your server:
https://discordapp.com/api/oauth2/authorize?client_id=526504376853069845&permissions=0&scope=bot


Running your own instance:
Have a discord app configured and a bot added.
Invite the bot to your channel
Copy the 'token' value  into a token.config file.
Run gel_bot.py


# Imouto_Bot
A discord bot that pulls images from various boorus.

Requires Discordpy rewrite version

Currently it is set to pull from the following boorus(?):

Gelbooru

Konachan

Yandere

Safebooru

Realbooru


I used Discordpy for the actual bot part.


Commands:
^gel - grab an image from gelbooru

^sfw - grab an image from safebooru

^yan - grab an image from yandere

^kona- grab an image from konachan

^real- grab an image from realbooru

^stats-print a list of which user has made the most successful requests.

Pass in a command with some tags as if you were searching on a booru and it will find a random image that satisfies those tags.
ex.
^gel black_hair game_cg cake

Pass in a '-' before a tag to exclude that tag from the search

Pass in a '~' before a tag to find tags that are similar to that tag(incase you spelled it wrong)


Obviously this is an NSFW bot as all the imageboards except for safebooru host 18+ content.
