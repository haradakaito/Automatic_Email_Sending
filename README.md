# 定時メール自動送信プログラム
## 0. システム概要図
![システム概要_ver1 1 0](https://github.com/haradakaito/Automatic_Email_Sending/assets/75819611/5c1dc72e-51ff-4c23-b7ef-180dad5381ed)

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
