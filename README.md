# 定時メール自動送信プログラム
## 0. システム概要図
![画像1](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/6d277790-c7c0-4ecf-a486-e532dde7f4d6)

## 1. 仕様定義
- 毎日20:00に自動でメールを送信する
- GoogleCalendarで管理されているユーザーの予定を参照し，メール本文に記載する
- Notionで管理されている内容を参照し，メール本文に記載する
- Notionで管理されている情報を参照し，送信アドレスを取得する
- メール送信の旨をLINEで通知する
- ユーザー追加による拡張が可能
- 一つのプログラムで全ユーザー分送信が可能
- Windows/RaspberryPiOSで動作可能
## 2. 初期設定

### 1. Google Calendarの非公開ical URLを取得  
configファイル内URLを保存(config/credentials.json)
### 2. Notion API 取得  
### 3. Line Notify API 取得  
### 4. configファイル編集  
config/config.jsonファイルを以下の項目を更新  
「LineNotify関連・NotionAPI関連・所属・日報送信先」

### 5. 定期実行プログラム開始
###  Windows
```
$ pip install -r requirements.txt
$ python lib/master-win.py
```
### Raspberry Pi OS
```
$ sudo bash install.sh
```

## 3. ユーザー追加方法
![ユーザー追加方法](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/2e5bba75-fbf8-439d-8d94-368556518977)
