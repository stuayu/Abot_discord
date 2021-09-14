from __future__ import unicode_literals
import youtube_dl
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
    #'cookiefile': '/app/cookies.txt',
    #'proxy': 'XXXXXXXXXXXXXXXXXXXXXXXXX',
    'verbose': 'True',
    'logger': logger,
    'source_address': '0.0.0.0',
    'noplaylist': 'True',
    'socket_timeout': 30,
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s.webm',
}

ydl_opts2 = {
    'format': 'bestaudio[acodec=opus]/bestaudio/best -x',
    'logger': MyLogger(),
    #'cookiefile': '/app/cookies.txt',
    'noplaylist': 'True',
    'verbose': 'True',
    'logger': logger,
    'source_address': '0.0.0.0',
    'socket_timeout': '30',
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s.webm',
}

ydl_opts3 = {
    'format': 'bestaudio[acodec=opus]/bestaudio/best -x',
    'logger': MyLogger(),
    'verbose': 'True',
    'logger': logger,
    'noplaylist': 'True',
    'source_address': '0.0.0.0',
    'socket_timeout': '30',
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_DIR+'%(id)s.webm',
}

playlist_opt1 = {
    'extract_flat': 'in_playlist',
    'dumpjson': 'True',
}

playlist_opt2 = {
    'extract_flat': 'in_playlist',
    'dumpjson': 'True',
    #'cookiefile': '/app/cookies.txt',
    'proxy': 'XXXXXXXXXXXXXXXXXXXXXX',
}


def dl_music(url):
    if 'youtu' in url:
        logger.debug('youtube login')
        try:
            with youtube_dl.YoutubeDL(ydl_opts2) as ydl:
                meta = ydl.extract_info(url, download=True)
                return meta
        except youtube_dl.utils.DownloadError:
            pass 
        except Exception as e:
            logger.debug(e.args)
            return -1

        try:
            logger.debug('proxy youtube')
            with youtube_dl.YoutubeDL(ydl_opts1) as ydl:
                meta = ydl.extract_info(url, download=True)
                return meta
        except youtube_dl.DownloadError:
            pass
        except Exception as e:
            logger.debug(e.args)
            return -1

    else:
        with youtube_dl.YoutubeDL(ydl_opts3) as ydl:
            meta = ydl.extract_info(url, download=True)
        return meta

def playlist(url):
    try:
        with youtube_dl.YoutubeDL(playlist_opt1) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            o = json.loads(json.dumps(info_dict, ensure_ascii=False))
        return o
    except youtube_dl.utils.DownloadError:
            pass 
    except Exception as e:
        logger.debug(e.args)
        return -1

    try:
        with youtube_dl.YoutubeDL(playlist_opt2) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            o = json.loads(json.dumps(info_dict, ensure_ascii=False))
        return o
    except Exception as e:
        logger.debug(e.args)
        return -1



if __name__ == '__main__':
    l_1 = 'https://www.youtube.com/watch?v=--41OGPMurU&list=RD--41OGPMurU&start_radio=1'
    music = 'https://www.youtube.com/watch?v=3a7KuNsrwog'
    meta = playlist(music)

    print(meta)
    print(meta['entries'][1]['url'])
    print(meta['entries'][1]['title'])
    print(len(meta['entries']))
