import json,re

with open('src/modules/settings.json', 'r', encoding='utf-8') as f:
    text = f.read()
re_text = re.sub(r'/\*[\s\S]*?\*/', '', text) # コメント付きJSONを読み込むため
setting = json.loads(re_text)

######### 設定ファイルからデータをロード ##########
AKITA = setting['akita']
FUKUSHIMA = setting['fukushima']
login_id = setting['rec_server_id']
login_pass = setting['rec_server_pass']
TOKEN = setting['token']
short_token = setting['short_token']
channel_list:list = setting['channel_id']

AKITA_STREAM = AKITA+'/api/streams/live/'

AKITA_EPG_REALTIME = AKITA + \
    '/api/schedules/broadcasting?isHalfWidth=true'

FUKUSHIMA_STREAM = FUKUSHIMA +'/api/streams/live/'

FUKUSHIMA_EPG_REALTIME = FUKUSHIMA + \
    '/api/schedules/broadcasting?isHalfWidth=true'
