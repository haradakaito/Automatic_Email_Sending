# 定時メール自動送信プログラム
## 0. システム概要図
![画像1](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/11d7e684-5137-4044-9622-69bb1764164d)

## 1. 仕様定義
- 毎日20:00に自動でメールを送信する
- GoogleCalendarで管理されているユーザーの予定を参照し，メール本文に記載する
- Notionで管理されている内容を参照し，メール本文に記載する
- Notionで管理されている情報を参照し，送信アドレスを取得する
- ユーザー追加による拡張が可能
- 一つのプログラムで全ユーザー分送信が可能
- Windows/RaspberryPiOSで動作可能
## 2. 初期設定
1. ライブラリインストール
```
$ pip install -r requirements.txt
```
2. Google Calendar API取得  
下記URL(https://www.coppla-note.net/posts/tutorial/google-calendar-api/)を参考にしてcredentials.jsonを取得  
configファイル内に保存(config/credentials.json)
3. Notion API 取得  
4. Line Notify API 取得  
5. configファイル編集  
config/config.jsonファイルを以下の項目を更新  
「LineNotify関連・NotionAPI関連・所属・日報送信先」
## 3. クラス定義

## 4. メイン文

## 5. 実行方法
```
$ python master.py
```

