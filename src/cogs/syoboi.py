from discord.ext import commands,tasks  # Bot Commands Frameworkのインポート
import discord
from discord.commands import slash_command, SlashCommandGroup, Option
import modules.syoboical as syobocal
import asyncio
import time
# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# コグとして用いるクラスを定義。
class Syoboi(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # 送ったコマンドを表示するだけ (クラスはselfが必須なため注意)
    @slash_command()
    async def a_prog(self, ctx: discord.ApplicationContext, arg: Option(str, description='何日後の予定かを数値で入力', choices=['0','1','2','3','4','5','6','7'],default='0')):
        """しょぼいカレンダーからアニメの放送予定を取得 引数:何日後の予定かを数値で入力 (defalt:0)"""
        data = await syobocal.anime_prog(arg)
        logger.debug(data)
        embed = discord.Embed(title="アニメの放送予定一覧です",
                              color=discord.Colour.red())
        
        for (title,a_list) in data:
            embed.add_field(name=title,value=a_list, inline=False)
        
        await ctx.respond(embed=embed)
        
# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Syoboi(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
