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
## 2. 必要ライブラリ一覧(標準ライブラリは除く)
```
# 手動でインストールする場合
$ pip install google-api-python-client==2.114.0 google-auth-httplib2==0.2.0 google-auth-oauthlib==1.2.0 jpholiday==0.1.8

# requirement.txtを指定してインストールする場合
$ pip install -r ./requirements.txt
```
## 3. クラス定義

## 4. メイン文

## 5. 実行方法
```
$ python send_daily_report_mail.py
```

