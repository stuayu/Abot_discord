# Abot_discord
- [Abot_discord](#abot_discord)
  - [コマンド一覧](#コマンド一覧)
  - [IssuesとPull requests方針](#issuesとpull-requests方針)
  - [手順](#手順)
  - [local環境での実行方法](#local環境での実行方法)
  - [HerokuでDockerを動かす場合](#herokuでdockerを動かす場合)

## コマンド一覧
詳細はソースコードのコメントアウトを確認してください。  
[ヘルプページ](./help.md)にコマンドを書きます。

## IssuesとPull requests方針
>基本的に受け付けております。

## 手順
1. 設定ファイルのコピーと各種設定を行う。
    ```bash
    cp src/modules/settings.json.template src/modules/settings.json
    ```
    コピーを行ったら、URL短縮サービス用のトークンとDiscord用のトークン、必要があれば地震通知用に`channel`にチャンネルIDを記入します。

## local環境での実行方法(通常)
1. pip install pipenvを実行し、pipenvをインストールする
2. プロジェクト直下に仮想環境を作るため、以下を実行し依存関係をインストールする。
  ```powershell
  $env:PIPENV_VENV_IN_PROJECT = "true"
  pipenv install
  ```
3. pipenv run startを実行し起動する。


## local環境での実行方法(Docker)
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