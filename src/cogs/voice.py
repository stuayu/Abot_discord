from logging import getLogger, StreamHandler, DEBUG ,INFO
import random
import discord
from discord.errors import ClientException
from discord.commands import slash_command, SlashCommandGroup, Option
from discord.ext import commands, pages  # Bot Commands Frameworkのインポート
from multiprocessing import Process
from playlist.selector import ck_data
import modules.y_dl as y_dl
import os
import shutil
import queue
import asyncio

SAVE_DIR = '/tmp/discordbot/music/'

# logを出すためのおまじない #
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


class Voice(commands.Cog):
    # Voiceクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.__queue = []              # urlとtitleのキューオブジェクト格納用
        self.__url = queue.Queue()    # FIFOキューの作成
        self.__title = queue.Queue()  # FIFOキューの作成
        self.__stop: bool = False      # stopチェック
        self.__loop: bool = False      # loopチェック
        self.__a_loop: bool = False    # a_loop動作チェック
        self.__channel_embed_list = []  # channelとembedのリスト

    #### スラッシュコマンドグループ定義エリア ####
    vmusic = SlashCommandGroup("vmusic", "曲を再生します")

    #### 関数定義エリア ####
    async def con_bot(ctx: discord.ApplicationContext):
        """Botをボイスチャンネルに入室させます。またキューの初期化処理"""
        voice_state = ctx.author.voice
        if (not voice_state) or (not voice_state.channel):
            # もし送信者がどこのチャンネルにも入っていないなら
            await ctx.respond("先にボイスチャンネルに入っている必要があります。")
            return
        channel = voice_state.channel  # 送信者のチャンネル
        try:
            await channel.connect()  # VoiceChannel.connect()を使用
        except:
            pass
        return

    async def discon_bot(ctx: discord.ApplicationContext):
        """botを退出させる"""
        if not ctx.voice_client:
            await ctx.respond("Botはこのサーバーのボイスチャンネルに参加していません。")
            return
        await ctx.voice_client.disconnect()
        return

    async def embed_check(self, ctx: discord.ApplicationContext, _text: str):
        """embed object 再編集のための処理"""
        i = -1
        if self.__channel_embed_list:
            for _id, _embed, _send_massage in self.__channel_embed_list:
                i += 1
                if ctx.channel_id == _id:
                    embed = _embed
                    send_massage = _send_massage
                    break
            try:
                embed.description = _text
                await send_massage.edit(embed=embed)
            except:
                del self.__channel_embed_list[i]
                embed = discord.Embed(
                    color=discord.Colour.red(), description=_text)
                send_massage = await ctx.respond(embed=embed)
                self.__channel_embed_list.append(
                    [ctx.channel_id, embed, send_massage])
        else:
            embed = discord.Embed(
                color=discord.Colour.red(), description=_text)
            send_massage = await ctx.respond(embed=embed)
            self.__channel_embed_list.append(
                [ctx.channel_id, embed, send_massage])
            try:
                await ctx.delete()
            except:
                pass

        logger.debug('チャンネルデータ:'+str(self.__channel_embed_list))

    #### スラッシュコマンド定義エリア ####

    @slash_command()
    async def v_connect(self, ctx: discord.ApplicationContext):
        """Abotをボイスチャットに入室"""
        await ctx.defer()
        await ctx.delete()
        await Voice.con_bot(ctx=ctx)
        # await ctx.respond("success")
        return

    @slash_command()
    async def v_d(self, ctx: discord.ApplicationContext):
        """Abotをボイスチャットから切断する"""
        await ctx.defer()
        await ctx.delete()
        await Voice.discon_bot(ctx=ctx)
        # await ctx.respond("success")

    @vmusic.command()
    async def v_music(self,
                      ctx: discord.ApplicationContext,
                      url: Option(str, description="再生したいURLを入力してください", required=True)):
        """youtube-dlpに対応したサイトから音楽を再生 v_music URL"""
        await ctx.defer()
        await ctx.delete()
        logger.debug(url)

        await Voice.embed_check(self=self, ctx=ctx, _text='Now downloading ...')
        if 'nicovideo' in url:
            await Voice.embed_check(self=self, ctx=ctx, _text='ニコニコ動画のサイトは処理がとても遅いのでしばらくお待ち下さい')
        data = y_dl.dl_music(url)
        if type(data) is str:
            await ctx.respond('`'+data+'`')
            return
        m_file = SAVE_DIR+data['id']+'.webm'
        print(m_file)
        tmp = SAVE_DIR+data['id']+'--tmp.webm'
        await Voice.embed_check(self=self, ctx=ctx, _text='Start conversion by ffmpeg ...')

        while os.path.isfile(tmp):
            await asyncio.sleep(1)
        await Voice.embed_check(self=self, ctx=ctx, _text='['+data['title']+']('+url+')')

        source = await discord.FFmpegOpusAudio.from_probe(m_file)
        for _ in range(2):
            try:
                # すでに再生している場合は割り込み許可
                if ctx.voice_client.is_playing():
                    ctx.voice_client.stop()
                ctx.voice_client.play(source)
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)
                    if self.__loop == True:
                        ctx.voice_client.play(source)
                break
            except Exception as e:
                await Voice.con_bot(ctx=ctx)
        return

    @vmusic.command()
    async def a_loop(self, ctx: discord.ApplicationContext,
                     ck_list: Option(str, description='再生リストを指定してください', choices=["all", "yoasobi", "first_take", "porno", "anime", "a_2021_summer", "ikimono", "yorushika"], default="all", required=True),
                     rand_ck: Option(str, description='再生の方法を選択してください', choices=["True", "False"], default="True", required=True)):
        """プレイリスト(a_loop)をランダムに再生する

        Args:
            <ck_list> <str>:
                再生リスト指定 (v_music a_loop <再生リスト指定>)
                all             :全曲再生
                yoasobi         :YOASOBIの楽曲
                first_take      :THE FIRST TAKEの楽曲
                porno           :ポルノグラフィティの楽曲
                anime           :アニソン全般
                a_2021_summer   :2021夏アニメ
                ikimono         :いきものがかり
                yorushika       :ヨルシカ

            <rand_ck> <bool>:
                ランダム再生   (v_music a_loop <再生リスト指定> <ランダム再生>)
                True  or 1  :ランダム再生
                False or 0  :順次再生
        """
        try:
            await ctx.defer()
            await ctx.delete()
        except:
            pass
        logger.debug('subcommand a_loop start ...')
        self.__a_loop = True  # a_loop 動作開始

        # すでに再生している場合は割り込み許可
        logger.debug('割り込みチェック')
        for _ in range(2):
            try:
                if ctx.voice_client.is_playing():
                    await Voice.v_stop(self,ctx,rm_music='False')
                    self.__loop = False
                break
            except Exception as e:
                await Voice.con_bot(ctx=ctx)
                logger.debug(e.args[0])
        # 初期化
        logger.debug('初期化処理開始')
        next_m = ''
        use_play = await ck_data(ck_list)
        max = len(use_play)-1
        while True:
            logger.debug('ループ開始')
            logger.debug('playing:'+str(ctx.voice_client.is_playing())+'\npaused:'+str(ctx.voice_client.is_paused()))
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                await asyncio.sleep(1)
            elif not ctx.voice_client.is_playing() and self.__loop == False:
                if self.__stop:
                    self.__stop = False
                    self.__a_loop = False
                    next_m = ''

                if next_m == '' and (rand_ck == 'True' or rand_ck == '1'):
                    logger.debug('最初の曲データをロード中')
                    next_m = use_play[random.randint(0, max)]
                    logger.debug('ロード成功:'+next_m)
                elif next_m == '' and (rand_ck == 'False' or rand_ck == '0'):
                    logger.debug('最初の曲データをロード中')
                    index_m = 0  # 再生楽曲の場所のインデックス
                    next_m = use_play[index_m]
                    logger.debug('ロード成功:'+next_m)
                elif len(next_m) > 5:
                    logger.debug('URLチェック通過')
                    pass
                else:
                    next_m = use_play[random.randint(0, max)]
                    rand_ck = 'True'
                    await ctx.respond('`正しいランダムオプションが指定されませんでした。 defaltで動作します。`')
                    # await ctx.respond_help('v_music a_loop')

                await Voice.embed_check(self=self, ctx=ctx, _text='Now downloading ...')

                data = y_dl.dl_music(next_m)

                if type(data) is str:
                    # 楽曲再生に失敗した場合の処理
                    await ctx.respond('`'+data+'`')
                    # 次の楽曲準備
                    if rand_ck == 'True':
                        next_m = use_play[random.randint(0, max)]
                    elif rand_ck == 'False':
                        index_m += 1
                        if index_m >= max:
                            next_m = use_play[index_m]
                            index_m = 0
                        next_m = use_play[index_m]
                    data = y_dl.dl_music(next_m)
                m_file = SAVE_DIR+data['id']+'.webm'
                tmp = SAVE_DIR+data['id']+'--tmp.webm'
                logger.debug(m_file)

                await Voice.embed_check(self=self, ctx=ctx, _text='Start conversion by ffmpeg ...')
                while os.path.isfile(tmp):
                    await asyncio.sleep(1)

                await Voice.embed_check(self=self, ctx=ctx, _text='['+data['title']+']('+next_m+')')

                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                try:
                    ctx.voice_client.play(source)
                except ClientException:
                    await Voice.v_connect(self, ctx)
                    ctx.voice_client.play(source)
                # 次の楽曲準備
                if rand_ck == 'True' or rand_ck == '1':
                    next_m = use_play[random.randint(0, max)]
                elif rand_ck == 'False' or rand_ck == '0':
                    index_m += 1
                    if index_m >= max:
                        next_m = use_play[index_m]
                        index_m = 0
                    next_m = use_play[index_m]
                p = Process(target=y_dl.dl_music, args=(next_m,))
                p.start()
            elif not ctx.voice_client.is_playing() and self.__loop == True:
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                ctx.voice_client.play(source)

    @slash_command()
    async def v_stop(self,
                     ctx: discord.ApplicationContext,
                     rm_music: Option(str, description='キャッシュ済み音楽データを削除する', choices=["True", "False"], default="False", required=True)):
        """音楽の再生を停止 (v0.0.6:停止時キャッシュ削除追加)
            Args:
                <rm_music> <bool>:
                    rm_music: キャッシュ済みの音楽データを削除するか
                    True or 1  : 削除
                    False or 0 : 残す(defalt)
        """
        try:
            await ctx.defer()
            await ctx.delete()
        except:
            pass
        for i in range(len(self.__channel_embed_list)-1):
            if ctx.channel.id == self.__channel_embed_list[i][0]:
                del self.__channel_embed_list[i]
                break
        #voice_client = ctx.message.guild.voice_client
        # await ctx.message.delete()
        if not ctx.voice_client.is_playing():
            await ctx.respond('再生されていません')
        ctx.voice_client.stop()
        self.__stop = True
        if rm_music == 'True' or rm_music == '1':
            shutil.rmtree(SAVE_DIR)
            os.mkdir(SAVE_DIR)
        return
        # await ctx.respond('stop!')

    @slash_command()
    async def v_skip(self,
                     ctx: discord.ApplicationContext,
                     skip_num: Option(str, description='スキップ数を指定します', default='1', required=True)):
        """音楽をスキップ"""
        await ctx.defer()
        await ctx.delete()
        if int(skip_num) == 1:
            pass
        elif int(skip_num) <= 0:
            return 0
        else:
            for i in range(int(skip_num) - 1):
                self.__url.get()
                self.__title.get()

        ctx.voice_client.stop()
        await ctx.response()
        return
        # await ctx.respond('skip!')

    @slash_command()
    async def v_pause(self, ctx: discord.ApplicationContext):
        """音楽の再生をポーズする"""
        await ctx.defer()
        #voice_client = ctx.message.guild.voice_client
        await ctx.delete()
        ctx.voice_client.pause()
        await ctx.respond('pause!\n再開時はv_restartを')

    @slash_command()
    async def v_loop(self, ctx: discord.ApplicationContext):
        """再生中の楽曲をループさせます"""
        await ctx.defer()
        # await ctx.message.delete()
        if self.__loop == True:
            self.__loop = False
            await ctx.respond('loop stop!')
        else:
            self.__loop = True
            await ctx.respond('loop start!')

    @slash_command()
    async def v_restart(self, ctx: discord.ApplicationContext):
        """ポーズした楽曲を再生する"""
        await ctx.defer()
        await ctx.delete()
        #voice_client = ctx.message.guild.voice_client
        ctx.voice_client.resume()
        await ctx.response()
        # await ctx.respond('restart!')

    @slash_command()
    async def rm_tmp(self, ctx: discord.ApplicationContext):
        """手動でキャッシュを削除"""
        await ctx.defer()
        #voice_client = ctx.message.guild.voice_client
        await ctx.delete()
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        shutil.rmtree(SAVE_DIR)
        os.mkdir(SAVE_DIR)
        await ctx.respond('```' + 'musicフォルダ内を消しました' + '```')

    @slash_command()
    async def v_add(self,
                    ctx: discord.ApplicationContext,
                    url_list: Option(str, description='URLを入力してください(複数可)')):
        """キューに楽曲を追加 引数:URL (v0.0.7:複数URL対応)"""
        await ctx.defer()
        logger.info(url_list)
        args = str(url_list).split()

        for data in args:
            # 再生リストに追加
            if 'youtu' in data and 'list' in data:
                p_json = y_dl.playlist(data)
                if type(p_json) is str:
                    await ctx.respond('`'+p_json+'`')
                    return
                for i in range(len(p_json['entries'])):
                    y_url = 'https://youtu.be/' + p_json['entries'][i]['url']
                    y_title = p_json['entries'][i]['title']
                    logger.debug(y_url)
                    self.__url.put(y_url)
                    self.__title.put(y_title)
                await ctx.respond('追加しました\n現在キューに'+str(self.__url.qsize())+'件あります。')
                with self.__url.mutex:
                    p = Process(target=y_dl.dl_music,
                                args=(self.__url.queue[0],))
                    p.start()

            else:
                meta = y_dl.playlist(data)
                if type(meta) is str:
                    await ctx.respond('`'+meta+'`')
                    return
                self.__title.put(meta['title'])
                self.__url.put(data)
                await ctx.respond('追加しました\n現在キューに'+str(self.__url.qsize())+'件あります。')
                with self.__url.mutex:
                    p = Process(target=y_dl.dl_music,
                                args=(self.__url.queue[0],))
                    p.start()

    @slash_command()
    async def v_qplay(self, ctx: discord.ApplicationContext):
        """キューにある楽曲を再生"""
        await ctx.defer()
        await ctx.delete()
        # すでに再生している場合は割り込み許可
        try:
            if ctx.voice_client.is_playing():
                Voice.v_stop(self,ctx,rm_music='False')
        except:
            Voice.con_bot(ctx=ctx)
            pass

        if self.__url.empty():
            await ctx.respond('キューに何もありません')
            return

        while not self.__url.empty() or ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                # 音楽再生中orポーズ中に動作
                await asyncio.sleep(1)
            elif not ctx.voice_client.is_playing() and self.__loop == False:
                # 音楽がストップand単体ループが無効状態の時
                if self.__stop:  # v_stopが実行されたら
                    self.__stop = False
                    if not self.__url.empty():
                        with self.__url.mutex:
                            p = Process(target=y_dl.dl_music,
                                        args=(self.__url.queue[0],))
                            p.start()
                    break
                # 以下音楽再生処理
                url_m = self.__url.get()
                data = y_dl.dl_music(url_m)
                if type(data) is str:
                    await ctx.respond('`'+data+'`')
                    return
                m_file = SAVE_DIR+data['id']+'.webm'
                logger.debug(m_file)
                tmp = SAVE_DIR+data['id']+'--tmp.webm'
                while os.path.isfile(tmp):
                    await asyncio.sleep(1)
                embed = discord.Embed(color=discord.Colour.red(
                ), description='['+self.__title.get()+']('+url_m+')')
                await ctx.respond(embed=embed)
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                ctx.voice_client.play(source)
                if not self.__url.empty():
                    with self.__url.mutex:
                        # マルチスレッドで処理(処理待ちは行わない)
                        p = Process(target=y_dl.dl_music,
                                    args=(self.__url.queue[0],))
                        p.start()

            elif not ctx.voice_client.is_playing() and self.__loop == True:
                # 単体ループが有効の時
                source = await discord.FFmpegOpusAudio.from_probe(m_file)
                ctx.voice_client.play(source)

    @slash_command()
    async def v_qck(self, ctx: discord.ApplicationContext):
        """キューにある楽曲とURLを10件まで表示する。"""
        await ctx.defer()
        if self.__a_loop:
            embed = discord.Embed(
                title="a_loopを再生中", description="[a_loopの楽曲はこちらをご覧ください](https://github.com/stuayu/Abot_discord/blob/main/src/playlist/)", color=discord.Colour.red())
            await ctx.respond(embed=embed)
            return
        l_data = ''
        with self.__url.mutex:
            with self.__title.mutex:
                for i in range(len(self.__url.queue)):
                    if i <= 9:
                        l_data += str(i+1) + '|' + \
                            self.__title.queue[i] + ' | ' + \
                            '  ' + self.__url.queue[i] + '\n'

        l_data += '\n10件以上は省略されます。'

        await ctx.respond('```現在キューに' + str(self.__url.qsize()) + '件あります。\n'+l_data+'```')

    @slash_command()
    async def v_qcr(self, ctx: discord.ApplicationContext):
        """キューを空にする"""
        await ctx.defer()
        # await ctx.message.delete()
        while not self.__url.empty():
            self.__title.get()
            self.__url.get()
        await ctx.respond('キューを消しました')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Voice(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
