import requests
import datetime
from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.commands import slash_command, SlashCommandGroup, Option
import modules.request as dl
import discord
# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG ,INFO
import json
from modules.settings import login_id,login_pass,AKITA,FUKUSHIMA

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


class RECSERVER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__akita_channel = RECSERVER.load_channel(url=AKITA)
        self.__fukushima_channel = RECSERVER.load_channel(url=FUKUSHIMA)
        logger.debug('Akita:\n'+str(self.__akita_channel))
        logger.debug('fukushima:\n'+str(self.__fukushima_channel))

    def login(url: str) -> str:
        payload = dict(username=login_id, password=login_pass)
        r = requests.post(url=url+"/token", data=payload)
        TOKEN = r.cookies['token']
        return TOKEN

    def time_to_date(unix_time):
        time = datetime.datetime.fromtimestamp(unix_time/1000)
        return time.strftime('%m/%d(%a) %H:%M')

    def POST(url: str, payload: dict, cookie: str):
        r = requests.post(url=url, data=payload, headers={
                          'cookie': 'token='+cookie, 'content-type': 'application/json'})
        return r.json()

    def load_channel(url: str):
        cookie = RECSERVER.login(url=url)
        r = requests.get(url=url+'/api/channels',
                         headers={'cookie': 'token='+cookie, 'content-type': 'application/json'})
        return r.json()

    def search_channel_name(self, channelId: int, regeon: str) -> str:
        if regeon == '秋田':
            channel_data = self.__akita_channel
        else:
            channel_data = self.__fukushima_channel
        logger.debug(str(len(channel_data)))
        for i in range(len(channel_data)):
            if channel_data[i]['id'] == channelId:
                channel_name = channel_data[i]['halfWidthName']
                break

        return channel_name

    @slash_command()
    async def prog_search(self,
                          ctx: discord.ApplicationContext,
                          search: Option(str, description='検索ワードを入力してください(正規表現が使えます)', required=True),
                          channel: Option(str, description='放送波種別を選択してください', choices=['All', 'GR', 'BS', 'CS'], default='All', required=False),
                          region: Option(str, description='リージョンを選択してください', choices=['秋田', '福島'], default='福島', required=False),
                          free: Option(str, description='無料番組のみを検索する', choices=['True', 'False'], default='True', required=False),
                          ):
        """EPGStationから番組検索"""
        #free='True'
        await ctx.defer()
        if region == '秋田':
            REGION = AKITA
        else:
            REGION = FUKUSHIMA

        if channel == 'GR':
            GR = True
            BS = False
            CS = False
        elif channel == 'BS':
            GR = False
            BS = True
            CS = False
        elif channel == 'CS':
            GR = False
            BS = False
            CS = True
        else:
            GR = True
            BS = True
            CS = True

        TOKEN = RECSERVER.login(REGION)
        logger.debug(TOKEN)
        payload = json.dumps({'isHalfWidth': True,
                              'limit': 300,
                              'option': {
                                  'BS': BS,
                                  'CS': CS,
                                  'GR': GR,
                                  'description': False,
                                  'extended': False,
                                  'isFree': bool(free),
                                  'keyCS': False,
                                  'keyRegExp': True,
                                  'keyword': search,
                                  'name': True
                              }
                              })
        logger.debug(payload)
        logger.debug(REGION+'/api/schedules/search')
        r = RECSERVER.POST(url=REGION+'/api/schedules/search',
                           payload=payload, cookie=TOKEN)
        search_result = []
        logger.debug(r)
        for i in range(len(r)):
            name = r[i]['name']
            channelname = RECSERVER.search_channel_name(self=self, channelId=r[i]['channelId'], regeon=region)
            description = r[i]['description']
            start = RECSERVER.time_to_date(r[i]['startAt'])
            end = RECSERVER.time_to_date(r[i]['endAt'])
            search_result.append([name, channelname, description, start, end])

        embed = discord.Embed(color=discord.Colour.red(), title='検索結果')

        for name, channelname, description, start, end in search_result:
            embed.add_field(name=name, value=channelname+'\n' +
                            start+'~'+end+'\n'+description, inline=False)

        await ctx.respond(embed=embed)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(RECSERVER(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
