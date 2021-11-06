import discord
import traceback  # エラー表示のためにインポート
import json
from discord.ext import commands

########### logを出すためのおまじない ###############
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
#####################################################
STATUS_MESSAGE = "Abot v0.2.0"
#####################################################
data = json.load(open('modules/settings.json', 'r'))
TOKEN = data['token']
# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.news',
    'cogs.message',
    'cogs.voice',
    'cogs.syoboi',
    'cogs.speedtest',
    'cogs.gif'
]

# prefixを修正する際にはここも直すこと
prefix = ','

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self,command_prefix,help_command):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix,help_command)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        logger.info('-----')
        logger.info(self.user.name)
        logger.info(self.user.id)
        await bot.change_presence(activity=discord.Game(name=STATUS_MESSAGE, type=1))
        logger.info('-----')

class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示 (v0.0.7:大幅改定)"

    def get_ending_note(self):
        data = '各コマンドの説明: '+prefix+'help <コマンド名>\n' \
                '各カテゴリの説明: '+prefix+'help <カテゴリ名>\n'

        return data
# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    # command_prefixはコマンドの最初の文字として使うもの。
    bot = MyBot(command_prefix=prefix,help_command=JapaneseHelpCommand())
    bot.run(TOKEN)  # Botのトークン
