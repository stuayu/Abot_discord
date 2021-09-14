from discord.ext import commands  # Bot Commands Frameworkのインポート
import requests
# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

SAVE_DIR = '/tmp/discordbot/img/'
# コグとして用いるクラスを定義。
class Message(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # 自分からのメッセージには返信しないように
        if message.author.bot:
            return
        else:
            # 添付ファイルの属性を処理
            if message.attachments:
                #await channel.send(str(message.attachments))
                logger.debug(str(message.attachments))
                # gets first attachment that user
                attachment = message.attachments[0]
                #await channel.send(attachment.url)
                logger.debug(attachment.url)

            #await channel.send(str(message.author.name)+"\n" +
            #      str(message.author.id)+"\n"+str(message.content))
            logger.debug(str(message.author.name)+"\n" +
                  str(message.author.id)+"\n"+str(message.content))

    # 送ったコマンドを表示するだけ (クラスはselfが必須なため注意)
    @commands.command()
    async def test(self, ctx,*,arg):
        """動作チェックのオウム返し(複数指定化 v0.0.6)"""
        await ctx.send(arg)

    @commands.command()
    async def syosetu(self, ctx):
        """小説サイトのurlを表示するだけ"""
        S_url = [['小説家になろう', 'https://yomou.syosetu.com/rank/genretop/', ],
                 ['カクヨム', 'https://kakuyomu.jp/rankings/all/entire']]

        tmp_list = ''
        for i in S_url:
            tmp_list += '・'+ i[0]+'\n'+'--<'+i[1]+'>--'+'\n'

        await ctx.send(tmp_list)

    @commands.command()
    async def getip(self,ctx):
        """IPアドレスを取得"""
        headers = {'User-Agent': 'curl'}
        res = requests.get('https://ifconfig.io/', headers=headers)
        ip = str(res.text.rstrip('\n'))
        logger.debug(ip)

        await ctx.send('`'+ip+'`')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Message(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
