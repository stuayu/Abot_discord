import requests
import os

# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


SAVE_DIR = '/tmp/discordbot/img/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
header = {
    'User-Agent': user_agent
}

def dl_data(url):
    r = requests.get(url, headers=header)

    if r.status_code != 200:
        e = Exception("HTTP status: " + r.status_code)
        raise e
    
    return r

def save_image(name: str, image: bytes):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    filename = SAVE_DIR + name
    with open(filename, "wb") as fout:
        fout.write(image)
    
    return 0

def dl_image(url, name: str):
    if os.path.exists(SAVE_DIR + name):
        logger.debug('すでにファイル'+SAVE_DIR+name+'が存在するためダウンロードをスキップしました。')
        return 0
    r = dl_data(url)
    chk = save_image(name, r.content)
    logger.debug('実行結果' + str(chk))
    return 0

    
