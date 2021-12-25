from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
from discord.commands import slash_command, SlashCommandGroup
import speedtest as st

# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Speedtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name='speedtest')
    async def speed_test(self, ctx: discord.ApplicationContext):
        """Herokuのネットワーク速度を表示する"""
        servers = []
        stest = st.Speedtest()
        stest.get_servers(servers)
        stest.get_best_server()

        down_result = stest.download()
        logger.debug(down_result)
        up_result = stest.upload()
        logger.debug(up_result)
        mbps_down_result = down_result / 1024 / 1024
        mbps_up_result = up_result / 1024 / 1024
        #result = [mbps_down_result, mbps_up_result]

        message = '```ダウンロード:'+str(mbps_down_result) + \
            'Mbps\n'+'アップロード:'+str(mbps_up_result)+'Mbps```'
        await ctx.respond(message)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Speedtest(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
