async def get_meidra_gif(title: str) -> str:
    """小林さんちのメイドラゴンのGIFのURL"""
    # https://maidragon.jp/news/archives/827
    # https://maidragon.jp/news/archives/1038
    return {
        'ha': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/13a658840a8373deb4355975b3e56e0b.gif',
        'thx': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/0ebccd3083a5445b85f0feeca1372b57.gif',
        'onegai': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a533a6932106c9f63ae9ee4ea3a478a5.gif',
        'gyu': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/58b9f8279c61a217bc7770446a6d542f.gif',
        'maken': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a5f64bc592c42aecea1e8fb29eac3642-2.gif',
        'bohe': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/806b36e95d491beec2aaaec7af98ad28-2.gif',
        'hello': 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/3f5592cb37efa6b1a0e1f5ac2cc86e26.gif'
    }.get(title)
