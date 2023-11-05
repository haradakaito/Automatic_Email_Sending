# 定時メール自動送信プログラム
　定時メール自動送信プログラムを作成することによって, 「毎日決められた時刻に決められたメールアドレスに対して送信する」という手間が省ける.   
　今回作成したメール自動送信システムの概要図を以下に示す. 
<img src=https://github.com/haradakaito/AutoMail/assets/75819611/6f4a9052-7bba-4ced-bdcb-db6fa11bcaac, width=500, align=right>
　今回作成したプログラム(auto_mail.py)は, Windows10/11で動作することを確認済みである.   
　指定したメールアドレスに対して, 進捗項目記録ファイル(progress.txt, progress_map.txt)から進捗項目を読み取り手メール本文に書き込むことで, 指定した時刻になると, メールを送信するという流れである.   
　利用した主要なライブラリを以下に示す. 
 - win32com.client
   ・・・Outlookインターフェース起動用
 - schedule
   ・・・任意時刻のプログラム実行用
 - jpholiday
   ・・・祝日判定用
 - datetime
   ・・・日付取得用・休日判定用
 - plyer
   ・・・送信完了通知送信用
