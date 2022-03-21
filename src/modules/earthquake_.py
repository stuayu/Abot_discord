# earthquake.py 変更前

import discord
import websockets
import json
import datetime
from header.logger import *
# https://www.p2pquake.net/json_api_v2/#/P2P%E5%9C%B0%E9%9C%87%E6%83%85%E5%A0%B1%20API/get_history



# 地震発生時刻の保存(一時的)
#earthquake_time = []
# 緊急地震速報のID
#emergency_earthquake_id = [(str, str)]


async def main():
    url = "wss://api.p2pquake.net/v2/ws"
    ws = await websockets.connect(url)
    res:dict = json.loads(await ws.recv())
    code = res['code']
    logger.info('code: '+str(code))
    logger.info('id: '+str(res['_id']))
    logger.debug(str(res))
    # 551(地震情報)、552(津波予報)、554(緊急地震速報 発表検出)、555(各地域ピア数)、561(地震感知情報)、9611(地震感知情報 解析結果)
    if code == 551:
        title,description = await earthquake_information(res)
    elif code == 552:
        title,description = await tsunami_forecast(res)
    elif code == 554:
        title,description = await Emergency_Earthquake_Report()
    else:
        title,description = None,None

    logger.info('title: %s',title)
    logger.info('description: %s',description)
    if title != None:
        return await create_embed(title,description,code)

async def create_embed(title:str,description:str,code:int):
    object_embed = discord.Embed(title=title,description=description,color=discord.Colour.red())
    if code != 554:
        return object_embed

async def analysis_earth(data):
    # 震源の深さ
    depth: int|str = data['earthquake']['hypocenter']['depth']
    # マグニチュード
    magnitude: float = data['earthquake']['hypocenter']['magnitude']
    # 震源の場所
    name: str = data['earthquake']['hypocenter']['name']
    # 最大震度
    maxscale: int = data['earthquake']['maxScale']
    # 地震発生時刻
    time = datetime.datetime.strptime(
        data['earthquake']['time'], '%Y/%m/%d %H:%M:%S')
    # 国内の津波について
    tsunami: str = data['earthquake']['domesticTsunami']

    if depth == -1:
        depth = '調査中'
    if name == None:
        name = '調査中'

    return depth, magnitude, name, maxscale, time, tsunami


async def select_scale(maxscale: int):
    if maxscale == -1:
        maxscale_str = '震度情報なし'
    elif maxscale == 10:
        maxscale_str = '震度1'
    elif maxscale == 20:
        maxscale_str = '震度2'
    elif maxscale == 30:
        maxscale_str = '震度3'
    elif maxscale == 40:
        maxscale_str = '震度4'
    elif maxscale == 45:
        maxscale_str = '震度5弱'
    elif maxscale == 46:
        maxscale_str = '震度5弱以上と推定'
    elif maxscale == 50:
        maxscale_str = '震度5強'
    elif maxscale == 55:
        maxscale_str = '震度6弱'
    elif maxscale == 60:
        maxscale_str = '震度6強'
    elif maxscale == 70:
        maxscale_str = '震度7'
    else:
        maxscale_str = '震度情報は定義されていません'

    return maxscale_str


async def select_tsunami(tsunami):
    if tsunami == 'None':
        res = 'なし'
    elif tsunami == 'Unknown':
        res = '不明'
    elif tsunami == 'Checking':
        res = '調査中'
    elif tsunami == 'NonEffective':
        res = '若干の海面変動が予想されるが、被害の心配なし'
    elif tsunami == 'Watch':
        res = '津波注意報'
    elif tsunami == 'Warning':
        res = '津波予報(種類不明)'

    return res


async def earthquake_information(data: dict):
    """地震情報解析"""
    # 地震情報の解析
    (depth, magnitude, name, maxscale, time, tsunami) = await analysis_earth(data)

    # 本文作成(震度4未満であれば終了)
    title = '地震が発生しました'
    description = '発生時刻:' + time.strftime('%Y年%m月%d日 %H:%M:%S') + '\n' \
        + '最大震度:' + await select_scale(maxscale) + '\n' \
        + '津波:' + await select_tsunami(tsunami) + '\n' \
        + '震源:' + name + '\n' \
        + '震源の深さ:' + str(depth)+'km\n' \
        + 'マグニチュード:' + str(magnitude) + '\n' \
        + '各地の地震情報:' + '\n' + await analysis_area(data)

    # 震度3以上を通知
    if maxscale < 30:
        return None,None

    logger.info(description)

    return title,description

async def check_scale(data,i):
    return data['points'][i]['pref']+data['points'][i]['addr']

async def analysis_area(data):
    scale1 = scale2 = scale3 = scale4 = scale5 = scale6 = scale7 = scale8 = scale9 = scale10 = ''
    for i in range(len(data['points'])):
        scale = data['points'][i]['scale']
        if scale == 10:
            scale1 += await check_scale(data,i) + ', '
        elif scale == 20:
            scale2 += await check_scale(data,i) + ', '
        elif scale == 30:
            scale3 += await check_scale(data,i) + ', '
        elif scale == 40:
            scale4 += await check_scale(data,i) + ', '
        elif scale == 45:
            scale5 += await check_scale(data,i) + ', '
        elif scale == 46:
            scale6 += await check_scale(data,i) + ', '
        elif scale == 50:
            scale7 += await check_scale(data,i) + ', '
        elif scale == 55:
            scale8 += await check_scale(data,i) + ', '
        elif scale == 60:
            scale9 += await check_scale(data,i) + ', '
        elif scale == 70:
            scale10 += await check_scale(data,i) + ', '

    description = ''
    if len(scale10) >= 3:
        description += '震度7: ' + scale10 + '\n'
    if len(scale9) >= 3:
        description += '震度6強: ' + scale9 + '\n'
    if len(scale8) >= 3:
        description += '震度6弱: ' + scale8 + '\n'
    if len(scale7) >= 3:
        description += '震度5強: ' + scale7 + '\n'
    if len(scale6) >= 3:
        description += '震度5弱以上と推定: ' + scale6 + '\n'
    if len(scale5) >= 3:
        description += '震度5弱: ' + scale5 + '\n'
    if len(scale4) >= 3:
        description += '震度4: ' + scale4 + '\n'
    if len(scale3) >= 3:
        description += '震度3: ' + scale3 + '\n'
    if len(scale2) >= 3:
        description += '震度2: ' + scale2 + '\n'
    if len(scale1) >= 3:
        description += '震度1: ' + scale1 + '\n'

    return description


async def tsunami_forecast(data):
    """津波情報解析"""
    title = '津波に関する情報'
    if data['cancelled'] == True:
        return title,'津波に関する警報・注意報は解除されました。'
    area_data = [(str, bool, str)]
    for i in range(len(data['areas'])):
        area_data.append(
            (data['areas'][i]['grade'], data['areas'][i]['immediate'], data['areas'][i]['name']))

    description:str = ''
    for grade, immediate, name in area_data:
        description += '種類: ' + await check_warning(grade) + '\n' \
            + '場所: ' + name + '\n'
    return title,description


async def check_warning(data):
    if data == 'MajorWarning':
        return '大津波警報(MajorWarning)'
    elif data == 'Warning':
        return '津波警報(Warning)'
    elif data == 'Watch':
        return '津波注意報(Watch)'
    else:
        return '不明'


async def Emergency_Earthquake_Report():
    """緊急地震速報解析"""
    # id,timeを保存
    description = '緊急地震速報が発表されました。強い地震に注意してください。'
    title = '緊急地震速報'
    return title,description
