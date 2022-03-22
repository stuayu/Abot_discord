from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.commands import slash_command, SlashCommandGroup
import modules.request as dl
from modules.meidora import get_meidra_gif
import discord
from header.logger import *

SAVE_DIR = '/tmp/discordbot/img/'
EXT_GIF = '.gif'

# https://maidragon.jp/news/archives/827
# https://maidragon.jp/news/archives/1038


class Gif(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #### スラッシュコマンドグループ定義エリア ####
    gif = SlashCommandGroup("gif", "gif関連")

    async def meidora_all(ctx: discord.ApplicationContext, filename: str):
        await ctx.defer()
        dl.dl_image(await get_meidra_gif(filename), filename+EXT_GIF)
        await ctx.respond(file=discord.File(SAVE_DIR+filename+EXT_GIF, filename+EXT_GIF))

    @gif.command(name='ha')
    async def meidora1(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='ha')

    @gif.command(name='thx')
    async def meidora2(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='thx')

    @gif.command(name='onegai')
    async def meidora3(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='onegai')

    @gif.command(name='gyu')
    async def meidora4(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='gyu')

    @gif.command(name='maken')
    async def meidora5(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='maken')

    @gif.command(name='bohe')
    async def meidora6(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='bohe')

    @gif.command(name='hello')
    async def meidora7(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await Gif.meidora_all(ctx, filename='hello')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Gif(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
