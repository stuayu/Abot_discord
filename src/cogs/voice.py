from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
from multiprocessing import Pool,Process
import modules.y_dl as y_dl
import os
import shutil
import queue
import asyncio

SAVE_DIR = '/tmp/discordbot/music/'

# logを出すためのおまじない #
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Voice(commands.Cog):
    # Voiceクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.__url = queue.Queue()  # FIFOキューの作成
        self.__title = queue.Queue()  # FIFOキューの作成
        self.__stop:bool = False

    @commands.command()
    async def v_connect(self,ctx):
        """Abotをボイスチャットに入室"""
        # Botをボイスチャンネルに入室させます。
        voice_state = ctx.author.voice
        if (not voice_state) or (not voice_state.channel):
            #もし送信者がどこのチャンネルにも入っていないなら
            await ctx.send("先にボイスチャンネルに入っている必要があります。")
            return

        channel = voice_state.channel  # 送信者のチャンネル
        await channel.connect()  # VoiceChannel.connect()を使用
    
    @commands.command()
    async def v_d(self,ctx):
        """Abotをボイスチャットから切断する"""
        # Botをボイスチャンネルから切断します。
        voice_client = ctx.message.guild.voice_client

        if not voice_client:
            await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
            return

        await voice_client.disconnect()
        await ctx.send("ボイスチャンネルから切断しました。")

    @commands.command()
    async def v_music(self, ctx, arg):
        """youtube-dlに対応したサイトから音楽を再生 引数:URL"""
        # youtubeから音源再生
        voice_client = ctx.message.guild.voice_client
        
        data = y_dl.dl_music(arg)

        m_file = SAVE_DIR+data['id']+'.webm'
        print(m_file)
        await ctx.send('`'+data['title']+'`')
        source = await discord.FFmpegOpusAudio.from_probe(m_file)
        # すでに再生している場合は割り込み許可
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(source)

    @commands.command()
    async def v_stop(self, ctx):
        """音楽の再生を停止 (v0.0.6:停止時キャッシュ削除追加)"""
        voice_client = ctx.message.guild.voice_client
        if not voice_client.is_playing():
            await ctx.send('再生されていません')
        voice_client.stop()
        self.__stop = True
        shutil.rmtree(SAVE_DIR)
        os.mkdir(SAVE_DIR)
        await ctx.send('stop!')

    @commands.command()
    async def v_skip(self, ctx, arg = '1'):
        """音楽をスキップ 引数:int 件数 (defalt: 1)"""
        if self.__url.empty():
            await ctx.send('キューに何もありません')
        voice_client = ctx.message.guild.voice_client
        if int(arg) == 1:
            pass
        elif int(arg) <= 0:
            return 0
        else:
            for i in range(int(arg) - 1):
                self.__url.get()
                self.__title.get()

        voice_client.stop()
        await ctx.send('skip!')

    @commands.command()
    async def v_pause(self, ctx):
        """音楽の再生をポーズする"""
        voice_client = ctx.message.guild.voice_client
        voice_client.pause()
        await ctx.send('pause!\n再開時はv_restartを')
    
    @commands.command()
    async def v_restart(self, ctx):
        """ポーズした楽曲を再生する"""
        voice_client = ctx.message.guild.voice_client
        voice_client.resume()
        await ctx.send('restart!')

    @commands.command()
    async def rm_tmp(self, ctx):
        """手動でキャッシュを削除"""
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        shutil.rmtree(SAVE_DIR)
        os.mkdir(SAVE_DIR)
        await ctx.send('```' + 'musicフォルダ内を消しました' + '```')
        
    @commands.command()
    async def v_add(self, ctx, *args):
        """キューに楽曲を追加 引数:URL (v0.0.7:複数URL対応)"""
        for data in args:
            #再生リストに追加
            if 'youtu' in data and 'list' in data:
                p_json = y_dl.playlist(data)
                for i in range(len(p_json['entries'])):
                    y_url = 'https://youtu.be/' + p_json['entries'][i]['url']
                    y_title = p_json['entries'][i]['title']
                    logger.debug(y_url)
                    self.__url.put(y_url)
                    self.__title.put(y_title)
                await ctx.send('追加しました\n現在キューに'+str(self.__url.qsize())+'件あります。')
                with self.__url.mutex:
                    p = Process(target=y_dl.dl_music, args=(self.__url.queue[0],))
                    p.start()
            else:
                meta = y_dl.playlist(data)
                self.__title.put(meta['title'])
                self.__url.put(data)
                await ctx.send('追加しました\n現在キューに'+str(self.__url.qsize())+'件あります。')
                with self.__url.mutex:
                    p = Process(target=y_dl.dl_music, args=(self.__url.queue[0],))
                    p.start()
        

    @commands.command()
    async def v_qplay(self, ctx):
        """キューにある楽曲を再生"""
        # youtubeから音源再生
        voice_client = ctx.message.guild.voice_client
        # すでに再生している場合は割り込み許可
        if voice_client.is_playing():
            await ctx.send('`,v_stopコマンドを実行の上再度お試しください`')
            return -1
        
        if self.__url.empty():
            await ctx.send('キューに何もありません')

        while not self.__url.empty() or voice_client.is_playing() or voice_client.is_paused():
            if voice_client.is_playing() or voice_client.is_paused():
                #await ctx.send('`曲は再生中です`')
                await asyncio.sleep(1)
                #print('曲は再生中です')
            elif not voice_client.is_playing():
                if self.__stop:
                    self.__stop = False
                    # 動画ファイルを削除
                    shutil.rmtree(SAVE_DIR)
                    os.mkdir(SAVE_DIR)
                    if not self.__url.empty():
                        with self.__url.mutex:
                            p = Process(target=y_dl.dl_music, args=(self.__url.queue[0],))
                            p.start()
                    break
                data = y_dl.dl_music(self.__url.get())

                m_file = SAVE_DIR+data['id']+'.webm'
                
                logger.debug(m_file)
                await ctx.send('`'+self.__title.get()+'`')
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                voice_client.play(source)
                if not self.__url.empty():
                    with self.__url.mutex:
                        p = Process(target=y_dl.dl_music, args=(self.__url.queue[0],))
                        p.start()

    @commands.command()
    async def v_qck(self, ctx):
        """キューにある楽曲とURLを10件まで表示する。"""
        l_data = ''
        with self.__url.mutex:
            with self.__title.mutex:
                for i in range(len(self.__url.queue)):
                    if i <= 9:
                        l_data += str(i+1) + '|' + self.__title.queue[i] + ' | ' + '  ' + self.__url.queue[i] + '\n'
                    
                
        l_data += '\n10件以上は省略されます。'
        
        await ctx.send('```現在キューに' + str(self.__url.qsize()) + '件あります。\n'+l_data+'```')
        
    @commands.command()
    async def v_qcr(self, ctx):
        """キューを空にする"""

        # キューからデータがなくなるまで取り出しを行う
        while not self.__url.empty():
            self.__title.get()
            self.__url.get()
        await ctx.send('キューを消しました')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Voice(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
