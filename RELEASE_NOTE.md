# リリースノート

## VER 1.0.0 (2022-XX-XX)
### 変更点
 - py-cordを使用したディスコードBOTです。
 - herokuにデプロイすることもできます。
 - ローカルでのdocker-compose環境での動作をサポートしています。
 - Discordのスラッシュコマンドに対応しています。
 - Youtube-dlpを利用した音楽の再生機能に対応しています。

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
|  v_connect  |  ボイスチャットに入室させます  |
|  v_d  |  ボイスチャットから切断します  |
|  vmusic v_music URL  |  youtube-dlpに対応したサイトから音楽を再生します URL:必須  |
|  vmusic a_loop ck_list rand_ck  |  [プレイリスト](https://github.com/stuayu/Abot_discord/tree/main/src/playlist)から再生します ck_list:必須 rand_ck:必須  |
|  v_stop rm_music  |  音楽の再生を停止  |
|  v_skip skip_num  |  音楽をスキップします  |
|  v_pause  |  音楽の再生をポーズする  |
|  v_loop  |  再生中の楽曲をループさせます  |
|  v_restart  |  ポーズした楽曲を再生する  |
|  rm_tmp  |  手動でキャッシュを削除  |
|  v_add url_list  |  キューに楽曲を追加 URL:必須  |
|  v_qplay  |  キューにある楽曲を再生  |
|  v_qck  |  キューにある楽曲とURLを10件まで表示する。  |
|  v_qcr  |  キューを空にする  |
|  a_prog arg  |  しょぼいカレンダーからアニメの放送予定を取得  |
|  speed_test  |  ネットワーク速度を表示する  |
|  ha  |   メイドラゴンGIF  |
|  thx  |   メイドラゴンGIF  |
|  onegai  |   メイドラゴンGIF  |
|  gyu  |   メイドラゴンGIF  |
|  maken  |   メイドラゴンGIF  |
|  bohe  |   メイドラゴンGIF  |
|  hello  |   メイドラゴンGIF  |