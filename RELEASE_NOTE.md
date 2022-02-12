# リリースノート

## VER 1.0.0 (2022-XX-XX)
### 変更点/概要
 - py-cordを使用したディスコードBOTです。
 - Discordの**スラッシュコマンド**に対応しています。
   - コマンドの詳細はスラッシュを入力すると表示されます。
 - herokuにデプロイすることもできます。
 - ローカルでのdocker-compose環境での動作をサポートしています。
 - Youtube-dlpを利用した音楽の再生機能に対応しています。
 - .m3u8ファイルの再生ができます。(URLアクセスできる場合)
 - Youtube Liveの再生が可能です。 
 - しょぼいカレンダーからスケジュール取得が可能です。

### 実装機能一覧
|  機能  |  説明  |
| ---- | ---- |
|  test 文字列  |  文字列をそのまま返します  |
|  check_ctx  |   チャンネルIDを返します  |
|  syosetu  |  小説サイトのURLを返します  |
|  getip  |  サーバのIPアドレスを取得し返します  |
|  release_note  |  リリースノートへのリンクを表示します  |
|  anews  |  秋田魁新報社のトップページから記事を表示する |
|  ynews  |  Yahooから記事を取得し表示します  |
|  nnews  |  NHKニュースを取得し表示します  |
|  vmusic connect  |  ボイスチャットに入室させます  |
|  vmusic d  |  ボイスチャットから切断します  |
|  vmusic d_all  |  ボイスチャットから全員切断します  |
|  vmusic play URL/region/channel  |  youtube-dlpに対応したサイトから音楽を再生する場合はURLのみ入力 region/channelは録画サーバを利用時  |
|  vmusic a_loop ck_list rand_ck  |  [プレイリスト](https://github.com/stuayu/Abot_discord/tree/main/src/playlist)から再生します ck_list:必須 rand_ck:必須  |
|  vmusic stop rm_music  |  音楽の再生を停止  |
|  vmusic skip skip_num  |  音楽をスキップします  |
|  vmusic pause  |  音楽の再生をポーズする  |
|  vmusic loop  |  再生中の楽曲をループさせます  |
|  vmusic restart  |  ポーズした楽曲を再生する  |
|  vmusic rm_tmp  |  手動でキャッシュを削除  |
|  vmusic q_add url_list  |  キューに楽曲を追加 URL:必須  |
|  vmusic qplay  |  キューにある楽曲を再生  |
|  vmusic qck  |  キューにある楽曲とURLを10件まで表示する。  |
|  vmusic qcr  |  キューを空にする  |
|  a_prog arg  |  しょぼいカレンダーからアニメの放送予定を取得  |
|  speed_test  |  ネットワーク速度を表示する  |
|  gif ha  |   メイドラゴンGIF  |
|  gif thx  |   メイドラゴンGIF  |
|  gif onegai  |   メイドラゴンGIF  |
|  gif gyu  |   メイドラゴンGIF  |
|  gif maken  |   メイドラゴンGIF  |
|  gif bohe  |   メイドラゴンGIF  |
|  gif hello  |   メイドラゴンGIF  |