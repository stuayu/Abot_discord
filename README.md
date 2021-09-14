# Abot_discord
詳細はソースコードのコメントアウトを確認してください。

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