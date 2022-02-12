import discord
import traceback  # エラー表示のためにインポート
from discord.ext import commands
from modules.settings import TOKEN

########### logを出すためのおまじない ###############
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
#####################################################
STATUS_MESSAGE = "Abot v0.9.0"
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

# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    # command_prefixはコマンドの最初の文字として使うもの。
    bot = MyBot()
    bot.run(TOKEN)  # Botのトークン
