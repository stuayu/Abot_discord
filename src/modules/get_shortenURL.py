# https://github.com/ihatasi/Discord_bot/blob/master/get_shortenURL.py から拝借
import requests
from modules.settings import short_token
# 短縮URLサービス

def get_shortenURL(longUrl):
    url = 'https://api-ssl.bitly.com/v3/shorten'
    access_token = short_token
    query = {
        'access_token': access_token,
        'longurl': longUrl
    }
    r = requests.get(url, params=query).json()['data']['url']
    return r
