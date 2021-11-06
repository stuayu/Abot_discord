from __future__ import unicode_literals
import random
import os
from multiprocessing import Process
#import youtube_dl
import yt_dlp
import json
import subprocess as sp

SAVE_DIR = '/tmp/discordbot/music/'
# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

proxy_ip_list = ['']

proxy_ip = proxy_ip_list[0]

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts1 = {
    'format': 'bestaudio[acodec=opus]/bestaudio/best -x',
    'logger': MyLogger(),
    'cookiefile': '/app/cookies.txt',
    #'proxy': proxy_ip,
    #'geo-bypass': 'True',
    #'geo-bypass-country': 'JP',
    'verbose': 'True',
    'logger': logger,
    #'source_address': '0.0.0.0',
    'noplaylist': 'True',
    'socket_timeout': 15,
    'retries': 0,
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s--tmp.webm',
}

ydl_opts2 = {
    'format': 'bestaudio[acodec=opus]/bestaudio/best/ba*/b -x',
    'logger': MyLogger(),
    'cookiefile': '/app/cookies.txt',
    #'geo-bypass': 'True',
    #'geo-bypass-country': 'JP',
    'retries': 0,
    'noplaylist': 'True',
    'verbose': 'True',
    'logger': logger,
    #'source_address': '0.0.0.0',
    'socket_timeout': 15,
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s--tmp.webm',
}

ydl_opts3 = {
    'format': 'bestaudio/best*[acodec!=none][abr>=192][height<=480]/best*[acodec!=none][height<=480]/ba*/best*[acodec!=none] -x',
    'logger': MyLogger(),
    'verbose': 'True',
    'logger': logger,
    'noplaylist': 'True',
    #'source_address': '0.0.0.0',
    'socket_timeout': 30,
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s--tmp.webm',
}

playlist_opt1 = {
    'extract_flat': 'in_playlist',
    'socket_timeout': 5,
    'retries': 0,
    #'geo-bypass': 'True',
    #'geo-bypass-country': 'JP',
    #'source_address': '0.0.0.0',
    'cookiefile': '/app/cookies.txt',
    'socket_timeout': 15,
    'dumpjson': 'True',
}

playlist_opt2 = {
    'extract_flat': 'in_playlist',
    'dumpjson': 'True',
    'cookiefile': '/app/cookies.txt',
    #'source_address': '0.0.0.0',
    #'geo-bypass': 'True',
    #'geo-bypass-country': 'JP',
    #'proxy': proxy_ip,
    'retries': 0,
    'socket_timeout': 30,
}


def dl_music(url:str):
    if 'youtu' in url:
        opt1 = os.path.isfile(SAVE_DIR+url.replace('https://www.youtube.com/watch?v=','')+'.webm')
        opt2 = os.path.isfile(SAVE_DIR+url.replace('https://youtu.be/','')+'.webm')
        logger.debug('youtube login')
        try:
            with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                if opt1 or opt2:
                    meta = ydl.extract_info(url, download=False)
                else:
                    meta = ydl.extract_info(url, download=True)
                    input = SAVE_DIR+meta['id']+'--tmp.webm'
                    output = SAVE_DIR+meta['id']+'.webm'
                    p = Process(target=ffmpeg_norm, args=(input,output,))
                    p.start()
                return meta
        except Exception as e:
            logger.debug(e.args[0])
            return e.args[0]
    elif 'nicovideo' in url:
        opt1 = os.path.isfile(SAVE_DIR+url.replace('https://www.nicovideo.jp/watch/','')+'.webm')
        logger.debug('niconico login')
        try:
            with yt_dlp.YoutubeDL(ydl_opts3) as ydl:
                if opt1:
                    meta = ydl.extract_info(url, download=False)
                else:
                    meta = ydl.extract_info(url, download=True)
                    input = SAVE_DIR+meta['id']+'--tmp.webm'
                    output = SAVE_DIR+meta['id']+'.webm'
                    p = Process(target=ffmpeg_norm, args=(input,output,))
                    p.start()
                return meta
        except Exception as e:
            logger.debug(e.args[0])
            return e.args[0]
            
    else:
        with yt_dlp.YoutubeDL(ydl_opts3) as ydl:
            meta = ydl.extract_info(url, download=True)
            input = SAVE_DIR+meta['id']+'--tmp.webm'
            output = SAVE_DIR+meta['id']+'.webm'
            p = Process(target=ffmpeg_norm, args=(input,output,))
            p.start()
        return meta

def playlist(url):
    try:
        with yt_dlp.YoutubeDL(playlist_opt1) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            o = json.loads(json.dumps(info_dict, ensure_ascii=False))
        return o
    except Exception as e:
        logger.debug(e.args[0])
        return e.args[0]
        pass

def ffmpeg_norm(source:str,output:str):
    """ffmpegを利用したノーマライズ"""
    cmd = 'ffmpeg -i ' + source +' -vn -af dynaudnorm '+ output
    logger.debug('ffmpeg cmd:'+cmd)
    proc = sp.run(cmd,stdout = sp.PIPE, stderr = sp.PIPE,shell=True)
    # 入力ファイル削除
    os.remove(source)
    logger.debug(proc.stdout.decode("utf8"))
    logger.debug(proc.stderr.decode("utf8"))

    return 0

if __name__ == '__main__':
    #meta = dl_music('https://www.youtube.com/watch?v=hH5d3riIHN4')
    #print(meta)
    l_1 = 'https://www.youtube.com/watch?v=--41OGPMurU&list=RD--41OGPMurU&start_radio=1'
    music = 'https://www.youtube.com/watch?v=3a7KuNsrwog'
    meta = playlist(music)

    print(meta)
    print(meta['entries'][1]['url'])
    print(meta['entries'][1]['title'])
    print(len(meta['entries']))
