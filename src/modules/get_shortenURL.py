# https://github.com/ihatasi/Discord_bot/blob/master/get_shortenURL.py から拝借
import requests
import json
# 短縮URLサービス
setting = json.load(open('src/modules/settings.json', 'r'))
token = setting['short_token']

def get_shortenURL(longUrl):
    url = 'https://api-ssl.bitly.com/v3/shorten'
    access_token = token
    query = {
        'access_token': access_token,
        'longurl': longUrl
    }
    r = requests.get(url, params=query).json()['data']['url']
    return r
