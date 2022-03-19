from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.commands import slash_command, SlashCommandGroup
import modules.request as dl
import discord
from header.logger import *

SAVE_DIR = '/tmp/discordbot/img/'

class Gif(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #### スラッシュコマンドグループ定義エリア ####
    gif = SlashCommandGroup("gif", "gif関連")

    @gif.command(name='ha')
    async def meidora1(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/13a658840a8373deb4355975b3e56e0b.gif'
        filename = 'meidora1.gif'
        dl.dl_image(url, filename)


        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))
    
    @gif.command(name='thx')
    async def meidora2(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url ='https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/0ebccd3083a5445b85f0feeca1372b57.gif'
        filename = 'meidora2.gif'
        dl.dl_image(url, filename)

        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))

    @gif.command(name='onegai')
    async def meidora3(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a533a6932106c9f63ae9ee4ea3a478a5.gif'
        filename = 'meidora3.gif'
        dl.dl_image(url, filename)

        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))

    
    @gif.command(name='gyu')
    async def meidora4(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/58b9f8279c61a217bc7770446a6d542f.gif'
        filename = 'meidora4.gif'
        dl.dl_image(url, filename)

        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))
    
    @gif.command(name='maken')
    async def meidora5(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a5f64bc592c42aecea1e8fb29eac3642-2.gif'
        filename = 'meidora5.gif'
        dl.dl_image(url, filename)

        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))

    @gif.command(name='bohe')
    async def meidora6(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/806b36e95d491beec2aaaec7af98ad28-2.gif'
        filename = 'meidora6.gif'
        dl.dl_image(url, filename)
        
        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))

    @gif.command(name='hello')
    async def meidora7(self, ctx: discord.ApplicationContext):
        """メイドラゴンGIF"""
        await ctx.defer()
        url = 'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/3f5592cb37efa6b1a0e1f5ac2cc86e26.gif'
        filename = 'meidora7.gif'
        dl.dl_image(url, filename)

        await ctx.respond(file=discord.File(SAVE_DIR+filename,filename))

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Gif(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
