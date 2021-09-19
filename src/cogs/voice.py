import random
from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
from multiprocessing import Pool,Process
import playlist.a_loop as m_list
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
        self.__loop:bool = False

    @commands.command()
    async def v_connect(self,ctx):
        """Abotをボイスチャットに入室"""
        # Botをボイスチャンネルに入室させます。
        voice_state = ctx.author.voice
        await ctx.message.delete()
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
        await ctx.message.delete()
        if not voice_client:
            await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
            return

        await voice_client.disconnect()
        #await ctx.send("ボイスチャンネルから切断しました。")

    @commands.group()
    async def v_music(self, ctx):
        """youtube-dlに対応したサイトから音楽を再生 v_music URL"""
        logger.debug(ctx.invoked_subcommand)

        if ctx.invoked_subcommand is None:
            url = str(ctx.message.content).split()[1]
            if not url or 'https://' not in url:
                await ctx.send_help('v_music')
                await ctx.send_help('v_music a_loop')
                return
            # youtubeから音源再生
            voice_client = ctx.message.guild.voice_client
            
            data = y_dl.dl_music(url)

            if type(data) is str:
                await ctx.send('`'+data+'`')
                return
            m_file = SAVE_DIR+data['id']+'.webm'
            print(m_file)
            tmp = SAVE_DIR+data['id']+'--tmp.webm'
            while os.path.isfile(tmp):
                await asyncio.sleep(1)
            await ctx.send('`'+data['title']+'`')
            source = await discord.FFmpegOpusAudio.from_probe(m_file)
            # すでに再生している場合は割り込み許可
            if voice_client.is_playing():
                voice_client.stop()
            voice_client.play(source)
            while voice_client.is_playing():
                await asyncio.sleep(1)
                if self.__loop == True:
                    voice_client.play(source)
            return

    @v_music.command()
    async def a_loop(self,ctx,ck_list:str = 'all',rand_ck:str = 'True'):
        """プレイリスト(a_loop)をランダムに再生する v_music a_loop
        オプション :
            再生リスト指定 (v_music a_loop <再生リスト指定>)
                利用可能機能:
                    all             :全曲再生
                    yoasobi         :YOASOBIの楽曲
                    first_take      :THE FIRST TAKEの楽曲
                    porno           :ポルノグラフィティの楽曲
                    anime           :アニソン全般
                    a_2021_summer   :2021夏アニメ
            ランダム再生   (v_music a_loop <再生リスト指定> <ランダム再生>)
                利用可能機能:
                    True    :ランダム再生
                    False   :順次再生
        """
        logger.debug('subcommand a_loop start ...')
        # youtubeから音源再生
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
        # すでに再生している場合は割り込み許可
        if voice_client.is_playing():
            await ctx.send('`,v_stopコマンドを実行の上再度お試しください`')
            return -1
        # 初期化
        next_m = ''
        use_play = await m_list.ck_data(ck_list)
        max = len(use_play)-1
        while True:
            if voice_client.is_playing() or voice_client.is_paused():
                await asyncio.sleep(1)
            elif not voice_client.is_playing() and self.__loop == False:
                if self.__stop:
                    self.__stop = False
                    next_m = ''
                    # 動画ファイルを削除
                    shutil.rmtree(SAVE_DIR)
                    os.mkdir(SAVE_DIR)
                    break
                if next_m == '' and rand_ck == 'True':
                    logger.debug('最初の曲データをロード中')
                    next_m = use_play[random.randint(0,max)]
                    logger.debug('ロード成功:'+next_m)
                elif next_m == '' and rand_ck == 'False':
                    logger.debug('最初の曲データをロード中')
                    index_m = 0 # 再生楽曲の場所のインデックス
                    next_m = use_play[index_m]
                    logger.debug('ロード成功:'+next_m)
                elif len(next_m) > 5:
                    pass
                else:
                    next_m = use_play[random.randint(0,max)]
                    rand_ck = 'True'
                    await ctx.send('`正しいランダムオプションが指定されませんでした。 defaltで動作します。`')
                    await ctx.send_help('v_music a_loop')
                data = y_dl.dl_music(next_m)
                if type(data) is str:
                    await ctx.send('`'+data+'`')
                    return
                m_file = SAVE_DIR+data['id']+'.webm'
                tmp = SAVE_DIR+data['id']+'--tmp.webm'
                logger.debug(m_file)
                while os.path.isfile(tmp):
                    await asyncio.sleep(1)
                await ctx.send('`'+data['title']+'`')
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                voice_client.play(source)
                # 次の楽曲準備
                if rand_ck == 'True':
                    next_m = use_play[random.randint(0,max)]
                elif rand_ck == 'False':
                    index_m += 1
                    if index_m >= max:
                        next_m = use_play[index_m]
                        index_m = 0
                    next_m = use_play[index_m]
                p = Process(target=y_dl.dl_music, args=(next_m,))
                p.start()
            elif not voice_client.is_playing() and self.__loop == True:
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                voice_client.play(source)

    @commands.command()
    async def v_stop(self, ctx):
        """音楽の再生を停止 (v0.0.6:停止時キャッシュ削除追加)"""
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
        if not voice_client.is_playing():
            await ctx.send('再生されていません')
        voice_client.stop()
        self.__stop = True
        shutil.rmtree(SAVE_DIR)
        os.mkdir(SAVE_DIR)
        #await ctx.send('stop!')

    @commands.command()
    async def v_skip(self, ctx, arg = '1'):
        """音楽をスキップ 引数:int 件数 (defalt: 1)"""
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
        if int(arg) == 1:
            pass
        elif int(arg) <= 0:
            return 0
        else:
            for i in range(int(arg) - 1):
                self.__url.get()
                self.__title.get()

        voice_client.stop()
        #await ctx.send('skip!')

    @commands.command()
    async def v_pause(self, ctx):
        """音楽の再生をポーズする"""
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
        voice_client.pause()
        await ctx.send('pause!\n再開時はv_restartを')

    @commands.command()
    async def v_loop(self, ctx):
        """再生中の楽曲をループさせます"""
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
        if self.__loop == True:
            self.__loop = False
        else:
            self.__loop = True
        await ctx.send('loop start!')

    @commands.command()
    async def v_restart(self, ctx):
        """ポーズした楽曲を再生する"""
        await ctx.message.delete()
        voice_client = ctx.message.guild.voice_client
        voice_client.resume()
        #await ctx.send('restart!')

    @commands.command()
    async def rm_tmp(self, ctx):
        """手動でキャッシュを削除"""
        voice_client = ctx.message.guild.voice_client
        await ctx.message.delete()
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
                if type(p_json) is str:
                    await ctx.send('`'+p_json+'`')
                    return
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
                if type(meta) is str:
                    await ctx.send('`'+meta+'`')
                    return
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
        await ctx.message.delete()
        # すでに再生している場合は割り込み許可
        if voice_client.is_playing():
            await ctx.send('`,v_stopコマンドを実行の上再度お試しください`')
            return -1
        
        if self.__url.empty():
            await ctx.send('キューに何もありません')

        while not self.__url.empty() or voice_client.is_playing() or voice_client.is_paused():
            if voice_client.is_playing() or voice_client.is_paused():
                await asyncio.sleep(1)
            elif not voice_client.is_playing() and self.__loop == False:
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
                if type(data) is str:
                    await ctx.send('`'+data+'`')
                    return
                m_file = SAVE_DIR+data['id']+'.webm'
                logger.debug(m_file)
                tmp = SAVE_DIR+data['id']+'--tmp.webm'
                while os.path.isfile(tmp):
                    await asyncio.sleep(1)
                await ctx.send('`'+self.__title.get()+'`')
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                voice_client.play(source)
                if not self.__url.empty():
                    with self.__url.mutex:
                        p = Process(target=y_dl.dl_music, args=(self.__url.queue[0],))
                        p.start()

            elif not voice_client.is_playing() and self.__loop == True:
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                voice_client.play(source)

    @commands.command()
    async def v_qck(self, ctx):
        """キューにある楽曲とURLを10件まで表示する。"""
        await ctx.message.delete()
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
        await ctx.message.delete()
        while not self.__url.empty():
            self.__title.get()
            self.__url.get()
        await ctx.send('キューを消しました')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Voice(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
