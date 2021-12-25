# Abot_discord
- [Abot_discord](#abot_discord)
  - [コマンド一覧](#コマンド一覧)
  - [IssuesとPull requests方針](#issuesとpull-requests方針)
  - [手順](#手順)
  - [local環境での実行方法](#local環境での実行方法)
  - [HerokuでDockerを動かす場合](#herokuでdockerを動かす場合)

## コマンド一覧
詳細はソースコードのコメントアウトを確認してください。  
helpの内容を下に置きます。
```
Gif:
  bohe      メイドラゴンGIF
  gyu       メイドラゴンGIF
  ha!       メイドラゴンGIF
  hello     メイドラゴンGIF
  maken     メイドラゴンGIF
  onegai    メイドラゴンGIF
  thx       メイドラゴンGIF
Message:
  check_ctx 動作チェックのオウム返し(複数指定化 v0.0.6)
  getip     IPアドレスを取得
  syosetu   小説サイトのurlを表示するだけ
  test      動作チェックのオウム返し(複数指定化 v0.0.6)
News:
  anews     秋田魁新報社のトップページから記事を表示する
  nnews     NHKニュースを表示する
  ynews     Yahooから記事を表示する
Speedtest:
  speedtest Herokuのネットワーク速度を表示する
Syoboi:
  a_prog    しょぼいカレンダーからアニメの放送予定を取得 引数:何日後の予定かを数値で入力 (defalt:0)
Voice:
  rm_tmp    手動でキャッシュを削除
  v_add     キューに楽曲を追加 引数:URL (v0.0.7:複数URL対応)
  v_connect Abotをボイスチャットに入室
  v_d       Abotをボイスチャットから切断する
  v_loop    再生中の楽曲をループさせます
  v_music   youtube-dlpに対応したサイトから音楽を再生 v_music URL
  v_pause   音楽の再生をポーズする
  v_qck     キューにある楽曲とURLを10件まで表示する。
  v_qcr     キューを空にする
  v_qplay   キューにある楽曲を再生
  v_restart ポーズした楽曲を再生する
  v_skip    音楽をスキップ
  v_stop    音楽の再生を停止 (v0.0.6:停止時キャッシュ削除追加)
​その他:
  help      コマンド一覧と簡単な説明を表示 (v0.0.7:大幅改定)

各コマンドの説明: ,help <コマンド名>
各カテゴリの説明: ,help <カテゴリ名>
```
## IssuesとPull requests方針
>基本的に受け付けております。

## 手順
1. 設定ファイルのコピーと各種設定を行う。
    ```bash
    cp src/modules/settings.json.template src/modules/settings.json
    ```
    コピーを行ったら、URL短縮サービス用のトークンとDiscord用のトークンを記入します。

2. ソースファイルの変更 (youtubeの年齢制限およびプロキシを行いたい方向け)
    `src/modules/y_dl.py`ファイル内にコメントアウトしてある `cookies`と`proxy`のコメントアウトを外してください。  
    また、cookiesファイルを `src/cookies.txt`に置きます。

## local環境での実行方法
1. Dockerをインストールする
2. Dockerを起動する。
    ```bash
    sudo docker-compose pull
    sudo docker-compose build
    sudo docker-compose up -d
    ```


## HerokuでDockerを動かす場合
1. Heroku cli をインストールする。
2. Herokuに登録する。
3. `powershell`でHerokuにログインする。
   `heroku login`
4. `heroku stack:set container -a 作成したアプリ名`
5. herokuにGithubと連携する設定を行う。
6. 実行時のログ確認法
   `heroku logs --tail -a アプリ名`