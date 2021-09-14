# https://github.com/ihatasi/Discord_bot/blob/master/get_news.py から拝借
import requests
import urllib.request
import re
from bs4 import BeautifulSoup

import modules.get_shortenURL as get_shortenURL

def get_news(url):

    # ユーザーエージェントを指定
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
        'AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/92.0.4515.159 Safari/537.36 '

    rest = requests.get(url, headers={'User-Agent': ua})

    # htmlパース
    soup = BeautifulSoup(rest.text, "html.parser")
    return soup
    
def get_akita_news():
    # 秋田魁新聞ニュース
    news_data = []

    url = 'https://www.sakigake.jp/'
    soup = get_news(url)

    data = soup.find_all(
        'a', class_='p-newslist-card__link p-newslist-card__link--rev')
    title_l = []
    body_l = []
    url_l = []
    for i in data:
        title = re.findall(
            '<h3 class="p-newslist-card__title">(.*)</h3>', str(i))
        title_l.append(title[0])
        body = re.findall(
            '<p class="p-newslist-card__desc">(.*)</p>', str(i))
        body_l.append(body[0])
        url = re.findall(
            '<a class="p-newslist-card__link p-newslist-card__link--rev" href=(.*)>', str(i))
        url_l.append(get_shortenURL.get_shortenURL('https://www.sakigake.jp'+url[0].replace('"', '')))

    return title_l,body_l,url_l
    

def get_yahoo_news():
    
    news_data = []
    url = 'https://www.yahoo.co.jp/'
    soup = get_news(url)
    # ヤフーニュースの見出しとURLの情報を取得して出力する
    data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
    for data in data_list:
        topic = data.span.string
        ynews_url = get_shortenURL.get_shortenURL(data.attrs["href"])
        news_data.append([topic,ynews_url])
        
    return news_data


def get_nhk_news():
    # ニュース格納用リスト
    news_data = []
    # urlの指定
    url = 'http://k.nhk.jp/knews/index.html'

    # ユーザーエージェントを指定
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) '\
        'AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Gecko/20100101 Firefox/60.0 '

    req = urllib.request.Request(url, headers={'User-Agent': ua})

    # htmlの取得
    html = urllib.request.urlopen(req)
    # htmlパース
    soup = BeautifulSoup(html, "html.parser")
    # 軽く中身だけを表示したいときはこっち
    # 簡易型NHKnewsへの変換
    text_data = []
    long_path = 'https://www3.nhk.or.jp/news/html/'
    news_path = 'http://k.nhk.jp/knews/'
    all_a = soup.find_all('a')
    all_a = all_a[:7]
    # 対象のURLを獲得
    for index in (all_a):
        n_url = news_path+index.get('href')
        l_url = long_path+index.get('href')
        news_data.append([index.contents[0], n_url, l_url])
    for data in news_data:
        url = data[1]
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        # htmlの取得
        html = urllib.request.urlopen(req)
        # htmlパース
        soup = BeautifulSoup(html, "html.parser")
        # title取得
        title_text = data[0]
        split_text = soup.text.split("\n")
        for target in range(len(split_text)):
            if(split_text[target].find("。") != -1):
                main_text = split_text[target]
                date_text = split_text[target+2] +\
                    '\n'+get_shortenURL.get_shortenURL(data[2])
        text_data.append([title_text, main_text, date_text, "-----"])
        # time.sleep(1)
        print("*")
    print("-----")
    return text_data, news_data


if __name__ == '__main__':
    (title,body,url) = get_akita_news()
    for i in range(len(title)):
        print(title[i])
        print(body[i])
        print(url[i])
        print('----------------------------------')
