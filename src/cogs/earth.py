from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.commands import slash_command, SlashCommandGroup
import modules.earthquake as earthquake
import discord
from header.logger import *
SAVE_DIR = '/tmp/discordbot/img/'


class earth(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.stop_code = 0

    async def core(self,ctx):
        while True:
            logger.info('loop 1')
            data = await earthquake.main()
            if self.stop_code == 1:
                break
            if data != None:
                logger.info('loop 2')
                try:
                    ctx.respond(data)
                except:
                    channel = self.bot.get_channel(845919275432017970)
                    await channel.send(data)
    
    @slash_command(guild_ids=[791951290258161685])
    async def start_earthquake(self, ctx: discord.ApplicationContext):
        """地震通知の有効化"""
        try:
            await ctx.defer()
            await ctx.delete()
        except:
            pass
        earth.core(self,ctx)
        logger.info('loop brake')
    
    @slash_command(guild_ids=[791951290258161685])
    async def stop_earthquake(self, ctx: discord.ApplicationContext):
        """地震通知の無効化"""
        await ctx.defer()
        await ctx.delete()
        self.stop_code = 1
        return



# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(earth(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
