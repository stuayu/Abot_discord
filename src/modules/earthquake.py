import discord
import websockets
import json
import datetime
from header.logger import *
# https://www.p2pquake.net/json_api_v2/#/P2P%E5%9C%B0%E9%9C%87%E6%83%85%E5%A0%B1%20API/get_history


async def main(res: dict):
    code = res['code']
    logger.info('code: '+str(code))
    logger.info('id: '+str(res['_id']))
    logger.debug(json.dumps(res, indent=2, ensure_ascii=False))
    # 551(地震情報)、552(津波予報)、554(緊急地震速報 発表検出)、555(各地域ピア数)、561(地震感知情報)、9611(地震感知情報 解析結果)
    if code == 551:
        title, description = await earthquake_information(res)
    elif code == 552:
        title, description = await tsunami_forecast(res)
    elif code == 554:
        title, description = await Emergency_Earthquake_Report()

    logger.info('title: %s', title)
    logger.info('description: %s', description)
    if title != None:
        res_emb = await create_embed(title, description, code)
        time = str(datetime.datetime.strptime(
            res['earthquake']['time'], '%Y/%m/%d %H:%M:%S').strftime('%Y%m%d%H%M%S'))
        _id = str(res['code'])+'_'+time  # --> ex: 551_202203280000
        return res_emb, _id  # データ, 情報IDを返す
    return None


async def connect_ws():
    """websocket通信の開始"""
    url = "wss://api.p2pquake.net/v2/ws"
    websocket = await websockets.connect(url)
    return websocket


async def recv_ws(websocket):
    """websocket通信のサーバーからデータ受信"""
    while True:
        data: dict = json.loads(await websocket.recv())
        logger.debug(data['code'])
        if data['code'] < 555:
            return data


async def create_embed(title: str, description: str, code: int):
    """通知用Embedの生成"""
    object_embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.red())

    if code != 554:
        return object_embed

    try:
        with open('src/modules/text_emergency.md', encoding='utf8') as f:
            value_d = f.read()  # 緊急地震速報時に追加できるマークダウンを定義(discord Embed表記が使えます)

        object_embed.add_field(name='追加メッセージ', value=value_d)
    except:
        logger.info('緊急地震速報時、追加メッセージを生成する箇所でエラーが発生しました。\nファイルが存在するか確認してください。')
        return object_embed

    return object_embed

#---------------------------------------------------------- 地震情報


async def analysis_earth(data):
    """地震情報の解析"""
    # 震源の深さ
    depth: int | str = data['earthquake']['hypocenter']['depth']
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
    else:
        depth = str(depth) + 'km'
    if name == '':
        name = '調査中'
    if magnitude == -1:
        magnitude = '調査中'

    return depth, magnitude, name, maxscale, time, tsunami


async def select_scale(maxscale: int):
    """震度情報の種類"""
    return {
        -1: '震度情報なし',
        10: '震度1',
        20: '震度2',
        30: '震度3',
        40: '震度4',
        45: '震度5弱',
        46: '震度5弱以上と推定',
        50: '震度5強',
        55: '震度6弱',
        60: '震度6強',
        70: '震度7',
    }.get(maxscale, '震度情報は定義されていません')


async def select_tsunami(tsunami: str):
    """地震による津波情報の種類"""
    return {
        'None': 'なし',
        'Unknown': '不明',
        'Checking': '調査中',
        'NonEffective': '若干の海面変動が予想されるが、被害の心配なし',
        'Watch': '津波注意報',
        'Warning': '津波予報(種類不明)',
    }.get(tsunami, '未定義')


async def earthquake_information(data: dict):
    """地震情報を埋め込みメッセージ用に変換"""
    # 地震情報の解析
    (depth, magnitude, name, maxscale, time, tsunami) = await analysis_earth(data)

    # 本文作成(震度2以下であれば終了)
    title = '地震が発生しました'
    description = '発生時刻:' + time.strftime('%Y年%m月%d日 %H:%M:%S') + '\n' \
        + '最大震度:' + await select_scale(maxscale) + '\n' \
        + '津波:' + await select_tsunami(tsunami) + '\n' \
        + '震源:' + name + '\n' \
        + '震源の深さ:' + depth + '\n' \
        + 'マグニチュード:' + str(magnitude) + '\n' \
        + '各地の地震情報:' + '\n' + await analysis_area(data)

    # 最大震度3以上かつ最大震度-1(不明)の場合は通知する
    if maxscale < 30 and maxscale > 0:
        return None, None

    logger.info(description)

    return title, description


async def analysis_area(data):
    """地震の大きさごとに地域をまとめる"""
    scale = {}
    scale_info = {
        10: '震度1',
        20: '震度2',
        30: '震度3',
        40: '震度4',
        45: '震度5弱',
        46: '震度5弱以上と推定',
        50: '震度5強',
        55: '震度6弱',
        60: '震度6強',
        70: '震度7',
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
    scale = dict(sorted(scale.items(), reverse=True))  # キー(震度)の大きい順に並び替え
    for i in scale.keys():
        # iにはscale(int)が入る
        if i < 30:  # 震度2以下は表示しない
            continue
        description += scale_info.get(i, '') + ': ' + scale.get(i, '') + '\n'

    return description


#---------------------------------------------------------- 津波情報
async def tsunami_forecast(data):
    """津波情報を埋め込みメッセージ用に変換"""
    title = '津波に関する情報'
    if data['cancelled'] == True:
        return title, '津波に関する警報・注意報は解除されました。'
    area_data = [(str, bool, str)]

    for item in data['areas']:
        area_data.append(
            (item['grade'], item['immediate'], item['name']))

    description: str = ''
    for grade, immediate, name in area_data:
        description += '種類: ' + await check_warning(grade) + '\n' \
            + '場所: ' + name + '\n'
    return title, description


async def check_warning(data: str):
    """津波情報の種類"""
    return {
        'MajorWarning': '大津波警報(MajorWarning)',
        'Warning': '津波警報(Warning)',
        'Watch': '津波注意報(Watch)',
    }.get(data, '不明')


#---------------------------------------------------------- 緊急地震速報
async def Emergency_Earthquake_Report():
    """緊急地震速報を埋め込みメッセージ用に変換"""
    description = '緊急地震速報が発表されました。強い地震に注意してください。'
    title = '緊急地震速報'
    return title, description
