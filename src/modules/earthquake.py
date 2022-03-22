import discord
import websockets
import json
import datetime
from header.logger import *
# https://www.p2pquake.net/json_api_v2/#/P2P%E5%9C%B0%E9%9C%87%E6%83%85%E5%A0%B1%20API/get_history

async def main():
    url = "wss://api.p2pquake.net/v2/ws"
    ws = await websockets.connect(url)
    res: dict = json.loads(await ws.recv())
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
    object_embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.red())

    if code != 554:
        return object_embed


#---------------------------------------------------------- 地震情報
async def analysis_earth(data):
    """地震情報の解析"""
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
    """地震情報の種類"""
    return {
        -1:'地震情報なし',
        10:'震度1',
        20:'震度2',
        30:'震度3',
        40:'震度4',
        45:'震度5弱',
        46:'震度5弱以上と推定',
        50:'震度5強',
        55:'震度6弱',
        60:'震度6強',
        70:'震度7',
    }.get(maxscale, '地震情報は定義されていません')


async def select_tsunami(tsunami: str):
    """地震による津波情報の種類"""
    return {
        'None':'なし',
        'Unknown':'不明',
        'Checking':'調査中',
        'NonEffective':'若干の海面変動が予想されるが、被害の心配なし',
        'Watch':'津波注意報',
        'Warning':'津波予報(種類不明)',
    }.get(tsunami, '未定義')


async def earthquake_information(data: dict):
    """地震情報を埋め込みメッセージ用に変換"""
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


async def analysis_area(data):
    """地震の大きさごとに地域をまとめる"""
    scale = {}
    scale_info = {
        10:'震度1',
        20:'震度2',
        30:'震度3',
        40:'震度4',
        45:'震度5弱',
        46:'震度5弱以上と推定',
        50:'震度5強',
        55:'震度6弱',
        60:'震度6強',
        70:'震度7',
    }
    for point in data['points']:

        # scaleのデータ構造の例
        # scale = {
        #   10 : "... 文字列 ...",
        #   45 : "... 文字列 ...",
        # }
        scale[int(point['scale'])] = scale.get(int(point['scale']), '')\
            + point['pref'] + point['addr']+', '

    description = ''
    for i in scale.keys():
        # iにはscale(int)が入る
        description += scale_info.get(i, '') + ': ' + scale.get(i, '') + '\n'

    return description


async def tsunami_forecast(data):
    """津波情報を埋め込みメッセージ用に変換"""
    title = '津波に関する情報'
    if data['cancelled'] == True:
        return title,'津波に関する警報・注意報は解除されました。'
    area_data = [(str, bool, str)]

    for item in data['areas']:
        area_data.append(
            (item['grade'], item['immediate'], item['name']))

    description:str = ''
    for grade, immediate, name in area_data:
        description += '種類: ' + await check_warning(grade) + '\n' \
            + '場所: ' + name + '\n'
    return title,description


async def check_warning(data: str):
    """津波情報の種類"""
    return {
        'MajorWarning':'大津波警報(MajorWarning)',
        'Warning':'津波警報(Warning)',
        'Watch':'津波注意報(Watch)',
    }.get(data, '不明')


async def Emergency_Earthquake_Report():
    """緊急地震速報を埋め込みメッセージ用に変換"""
    description = '緊急地震速報が発表されました。強い地震に注意してください。'
    title = '緊急地震速報'
    return title,description