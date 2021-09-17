import requests
import xml.etree.ElementTree as ET
import re
#import discord
#import asyncio
from datetime import datetime, timedelta, timezone

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

async def anime_prog(day):
    syoboical_xml = requests.get('https://cal.syoboi.jp/cal_chk.php')
    # XML解析
    root = ET.fromstring(syoboical_xml.content)
    now = datetime.now(JST)
    now_time = "{0:%Y%m%d%H%M%S}".format(now)
    # 要素「ProgItem」のデータを1つずつ取得
    day_o = "{0:%m%d}".format(now + timedelta(days=int(day)))
    day_m = "{0:%m%d%H%M}".format(now + timedelta(days=int(day)))
    anime_data=[]
    for ProgItem in root.iter('ProgItem'):
        #しょぼいカレンダーのチャンネルIDを指定して検索
        # https://cal.syoboi.jp/mng?Action=ShowChList
        # print(day_o)
        st = ProgItem.get('StTime')
        if int(day) == 0:
            if re.compile('1|2|4|5|6|15|16|17|18|71|128').fullmatch(ProgItem.get('ChID')) and st[4:8] == day_o and st[4:12] >= day_m:
                chname = ProgItem.get('ChName')
                title = ProgItem.get('Title')
                subtitle = ProgItem.get('SubTitle')
                number = ProgItem.get('Count')
                data = st[4:6] + '/' + st[6:8] + ' ' + st[8:10] + ':' + st[10:12] + ' 第'+number+'話 ' + subtitle + ' ' + chname
                anime_data.append([title, data])
        else:
            if re.compile('1|2|4|5|6|15|16|17|18|71|128').fullmatch(ProgItem.get('ChID')) and st[4:8] == day_o:
                chname = ProgItem.get('ChName')
                title = ProgItem.get('Title')
                subtitle = ProgItem.get('SubTitle')
                number = ProgItem.get('Count')
                data = st[4:6] + '/' + st[6:8] + ' ' + st[8:10] + ':' + \
                    st[10:12] + ' 第'+number+'話 ' + subtitle + ' ' + chname
                anime_data.append([title, data])
            
    return anime_data

"""
async def auto_anime_prog(day):
    syoboical_xml = requests.get('https://cal.syoboi.jp/cal_chk.php')
    # XML解析
    root = ET.fromstring(syoboical_xml.content)
    now = datetime.now(JST)
    now_time = "{0:%Y%m%d%H%M%S}".format(now)
    # 要素「ProgItem」のデータを1つずつ取得
    day_o = "{0:%m%d}".format(now + timedelta(days=int(day)))
    day_m = "{0:%m%d%H%M}".format(now + timedelta(days=int(day)))
    anime_data = []
    for ProgItem in root.iter('ProgItem'):
        #しょぼいカレンダーのチャンネルIDを指定して検索
        # https://cal.syoboi.jp/mng?Action=ShowChList
        # print(day_o)
        st = ProgItem.get('StTime')
        if int(day) == 0:
            if re.compile('1|2|4|5|6|15|16|17|18|71|128').fullmatch(ProgItem.get('ChID')) and st[4:8] == day_o and st[4:12] >= day_m:
                chname = ProgItem.get('ChName')
                title = ProgItem.get('Title')
                subtitle = ProgItem.get('SubTitle')
                number = ProgItem.get('Count')
                data = st[4:6] + '/' + st[6:8] + ' ' + st[8:10] + ':' + \
                    st[10:12] + ' 第' + number + '話 ' + subtitle + ' ' + chname
                time = st
                anime_data.append([title, data,time])
        else:
            if re.compile('1|2|4|5|6|15|16|17|18|71|128').fullmatch(ProgItem.get('ChID')) and st[4:8] == day_o:
                chname = ProgItem.get('ChName')
                title = ProgItem.get('Title')
                subtitle = ProgItem.get('SubTitle')
                number = ProgItem.get('Count')
                data = st[4:6] + '/' + st[6:8] + ' ' + st[8:10] + ':' + \
                    st[10:12] + ' 第'+number+'話 ' + subtitle + ' ' + chname
                time = st
                anime_data.append([title, data, time])

    return anime_data


async def auto(ctx):
    data = await auto_anime_prog(0)
    now = datetime.now(JST)
    diff = timedelta(minutes=5)
    anime_data = []
    text = 'まもなく次の番組が始まります'
    embed = discord.Embed(title=text, color=discord.Colour.red())

    for (title, a_list, time) in data:
        time = time + '+0900'
        time_tmp = datetime.strptime(time, '%Y%m%d%H%M%S%z')
        if (time_tmp - now) <= diff:
            anime_data.append([title, a_list])
    if anime_data == []:
        return 0
    else:
        for (title, a_list) in anime_data:
            embed.add_field(name=title, value=a_list, inline=False)
            await ctx.send(embed=embed)

        return 0
    
"""
    
if __name__ == '__main__':
    data = anime_prog('5')
    print(data)
