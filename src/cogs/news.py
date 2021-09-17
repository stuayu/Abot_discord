from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
import modules.get_news as get_news

# コグとして用いるクラスを定義。


class News(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    # @commands.command()
    # async def ping(self, ctx):
    #    await ctx.send('pong!')
    @commands.command()
    async def anews(self, ctx):
        """秋田魁新報社のトップページから記事を表示する"""
        embed = discord.Embed(title="秋田魁新報ニュースです。",
                              color=discord.Colour.red())
        (title, body, url) = get_news.get_akita_news()
        for i in range(len(title)):
            body[i] = body[i] + '\n' + url[i] + '\n----'
            embed.add_field(name='・'+title[i], value=body[i], inline=False)

        await ctx.send(embed=embed)
    # ヤフーのトップニュースを表示する

    @commands.command()
    async def ynews(self, ctx):
        """Yahooから記事を表示する"""
        await ctx.message.delete()
        await ctx.send("今日のYahooニュースです．")
        # Yahooトップのトピック記事タイトルを取得
        news_data = get_news.get_yahoo_news()
        top_news = ""
        for news in (news_data):
            top_news += '・'+news[0]+'\n'+'--<'+news[1] + '>--' + '\n'
        await ctx.send(top_news)

    # NHKのトップニュース
    @commands.command()
    async def nnews(self, ctx):
        """NHKニュースを表示する"""
        await ctx.message.delete()
        embed = discord.Embed(title="今日のNHKニュースです．",
                              color=discord.Colour.red())
        # NHKトップのトピック記事を取得
        text_data, news_data = get_news.get_nhk_news()
        # テキストデータのみの時
        text_ = ""
        for news in text_data:
            for target in news:
                if target.startswith('･'):
                    title = target
                else:
                    text_ += target + '\n'
            embed.add_field(name=title, value=text_, inline=False)
            text_ = ''
        await ctx.send(embed=embed)

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(News(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
