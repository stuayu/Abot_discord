import discord
import traceback  # エラー表示のためにインポート
from discord.ext import commands
from modules.settings import TOKEN, channel_list
from modules.earthquake import main, connect_ws, recv_ws
from header.logger import *

#####################################################
STATUS_MESSAGE = "Abot v0.9.5"
#####################################################
# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.news',
    'cogs.message',
    'cogs.voice',
    'cogs.syoboi',
    'cogs.speedtest',
    'cogs.gif',
    'cogs.recserver'
]

# prefixを修正する際にはここも直すこと
#prefix = '/'

# クラスの定義。ClientのサブクラスであるBotクラスを継承。


class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__()
        self.error_check = 0

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                self.error_check = -1
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        logger.info('-----')
        logger.info(self.user.name)
        logger.info(self.user.id)
        if self.error_check != 0:
            await bot.change_presence(activity=discord.Game(name='起動エラーが発生しています', type=1))
        else:
            await bot.change_presence(activity=discord.Game(name=STATUS_MESSAGE, type=1))
        logger.info('-----')

        # 送信済みの情報ID, メッセージIDを格納
        # ID_LOGGER = {
        #  "_id":[
        #    "message_id",
        #    "message_id", ...
        #  ],
        #  "_id":[], ...
        # }
        ID_LOGGER = {}

        websocket = await connect_ws()  # websocketのコネクション開始

        while True:
            data_ws = await recv_ws(websocket)
            data, _id = await main(data_ws)  # データ, 情報IDを受け取る

            if data != None:
                mes_id = []  # 一時的にメッセージIDを格納するリスト
                if _id in ID_LOGGER:
                    for i in ID_LOGGER.get(_id, []):
                        mes_id.append(await i.edit(embed=data))  # 送信内容の編集
                else:
                    for i in channel_list:
                        channel = bot.get_channel(i)
                        mes_id.append(await channel.send(embed=data))
                ID_LOGGER[_id] = mes_id  # 送信済みのメッセージIDリストの更新


# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    # command_prefixはコマンドの最初の文字として使うもの。
    bot = MyBot()
    bot.run(TOKEN)  # Botのトークン
