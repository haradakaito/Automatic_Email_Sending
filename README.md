# 定時メール自動送信プログラム
## 0. システム概要図
![システム概要_ver1 1 0](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/5c1dc72e-51ff-4c23-b7ef-180dad5381ed)

- **毎日メールを送信する**  
  毎日とは言っても，休祝日に送信するのは健全ではない．そのため，休祝日は送信をしないこととする．  
  ユーザー全員が全く同じ時間に送信するのは違和感がある．そのため，ユーザーごとに送信を行う時間を変えることとする．  
  メールは，各ユーザーのメールアドレスから特定のメールサーバーに対して送信することとする． 
- **ユーザーに通知する**  
  自分のメールがいつ送信されるのかが分かった方が確認がしやすく，プログラムが正常に動作しているか把握しやすい．そのため，各ユーザーが確認できるプラットフォーム上にユーザー名と通信予定時刻を通知することとする．
  仮に，一部のユーザーに不具合が生じた場合，該当するユーザーがそのことを把握するために，送信予定時刻の代わりに×を表示することとする．  
- **内容が毎日変わる**
  ユーザーは他のユーザー情報に対して干渉することができないこととする．  

## 1. システムフロー
### 1.1 LINE通知機能
![LINE通知](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/bab1d95e-8a61-40fc-b6d7-c0b7abb24e23)

### 1.2 メール情報取得
![メール情報取得までの流れ](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/f7cdacd4-aad7-4669-8008-e14ab2261e6f)

### 1.3 メール送信機能
![メール送信までの流れ](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/3d5c0fc4-2236-4485-a6a9-5de3d2f67b61)

### 2. 定期プログラムの実行方法
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

## Qiita記事
https://qiita.com/muumin_0525/items/6d7e81651d3b37e11183
