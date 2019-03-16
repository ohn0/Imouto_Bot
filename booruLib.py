class booruLib:
    GELBOORU  = 0x0
    REALBOORU = 0x1
    SFWBOORU  = 0x11

    apiEndpoints = {GELBOORU  : "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=",
                    REALBOORU : "https://realbooru.com/index.php?page=dapi&s=post&q=index&limit=",
                    SFWBOORU  : "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit="}



# https://gelbooru.com/ index.php?page=dapi&s=post&q=index&limit=
# https://realbooru.com/index.php?page=dapi&s=post&q=index