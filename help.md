## コマンド一覧を教えてください。

- 小林さんちのメイドラゴンのgif動画関連
    ```
    /gif ha
    /gif thx
    /gif onegai
    /gif gyu
    /gif maken
    /gif bohe
    /gif hello
    ```

- テストまたはツールコマンド
    ```
    /test 文字列  -> 文字列をそのまま表示
    /syosetu      -> 小説サイトを表示
    /getip        -> プログラムが動作しているコンピュータのIP表示
    /release_note -> リリースノートの表示
    /help         -> ヘルプサイトの表示
    /speedtest    -> サーバのスピードテスト
    ```

- ニュースサイトからコンテンツの取得を行う
    ```
    /anews        -> 秋田魁新報社から取得
    /ynews        -> Yahooから取得
    /nnews        -> NHKから取得
    ```

- 録画サーバ関連
    ```
    /prog_search search channel region free ->   
        search: 検索ワード(正規表現可)、channel: All,GR,BS,CS、
        region: 福島,秋田、free: True,False
    ```

- アニメ予定の表示
    ```
    /anime_syoboical date -> 
        指定日後のアニメの放送予定をしょぼいカレンダーから取得(当日は0を入力)
    ```
- ボイスチャット用
    ```
    /vmusic connect     -> botを入室
    /vmusic d           -> botのみ切断
    /vmusic d_all       -> 全員切断
    /vmusic play url region channel -> 音楽サイトから再生する場合はurlのみ
    /vmusic a_loop ck_list rand_ck  -> 以下にある楽曲一覧をランダム再生
    /vmusic stop        -> 再生停止
    /vmusic skip skip_num -> 楽曲スキップ
    /vmusic pause       -> 一時停止
    /vmusic loop        -> 楽曲ループ
    /vmusic restart     -> 一時停止楽曲を再生
    /vmusic q_add url_list -> キューに楽曲追加
    /vmusic qplay       -> キューの楽曲を再生
    /vmusic qck         -> キューの確認
    /vmusic qcr         -> キューの削除 
    ```
    [a_loopの楽曲一覧](https://github.com/stuayu/Abot_discord/tree/main/src/playlist)