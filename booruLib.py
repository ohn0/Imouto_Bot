class booruLib:
    GELBOORU  = 0x0
    REALBOORU = 0x1
    SFWBOORU  = 0x11
    KONACHAN  = 0x111
    YANDERE   = 0x100
    XBOORU    = 0x101
    R34       = 0x1111

    apiEndpoints = {GELBOORU  : "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=",
                    REALBOORU : "https://realbooru.com/index.php?page=dapi&s=post&q=index&limit=",
                    SFWBOORU  : "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=",
                    KONACHAN  : "http://konachan.com/post.json?limit=",
                    YANDERE   : "https://yande.re/post.json?limit=",
                    XBOORU    : "https://xbooru.com/index.php?page=dapi&s=post&q=index&limit=",
                    R34       : "https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit="}


