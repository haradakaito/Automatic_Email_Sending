# 定時メール自動送信プログラム
## 仕様定義
- 毎日20:00(休祝日を除く)にメールを送信する
- メールの件名は"年月日"を含む
- メールの本文はテキストファイルから取得する
- メールの本文は以下のように構成される
　- ヘッダー(進捗内容)
  - ボディ(進捗全体図)
  - フッター(次回のミーティングの月日)

## 使用ライブラリ一覧
- jpholiday
- datetime
- schedule
- time
- win32com

## クラス定義
Getterクラスでは，テキストファイルから取得する(get_text)，次回のミーティングの月日(get_plan)といった取得関係の関数が定義される
```python
class Getter:

    def get_text(self, path:str)

        ## テキスト(self.text_list)の取得 ##

        return self.text_list

    def get_plan(self):

        ## 今日の日付/曜日を取得 ##
        ## 次回のミーティングの月日(self.plan)を取得 ## -> GoogleCalendarAPIに変更予定

        return self.plan
```

Creatorクラスでは，Getterクラスで取得したテキストをメールの形式で作成するための作成関係の関数が定義される
```python
class Creator:

    # メール件名作成
    def create_subject(self):

        ## その日の日付を取得 ##
        ## 件名(self.subject)を作成 ##

        return self.subject

    # 本文作成
    def create_body(self, prog_list:list, progmap_list:list, plan_list:list):

        ## ヘッダー(self.head)の作成 ##
        ## ボディ(self.text)の作成 ##
        ## フッター(self.hoot)の作成 ##

        # 結合
        self.body = self.head+'\n'+self.text+'\n'+self.hoot

        return self.body
```
Senderクラスでは，Creatorクラスで作成したテキストを設定し，メールを送信する送信関係の関数が定義される
```python
# 送信関係
class Sender:

    ## メール送信 ##

        return True
```
## メイン文
```python
# 休祝日判定(休祝日: True)
def judge_holiday():
    if (jpholiday.is_holiday(datetime.date.today()) == True) or (datetime.datetime.now().weekday() == 5) or (datetime.datetime.now().weekday() == 6):
        return True
    else: return False

# メール送信(休祝日以外)
def send_mail():
    if judge_holiday() == False:

        getter, creator, sender = Getter(), Creator(), Sender()

        subject =  creator.create_subject() # 件名
        body = creator.create_body(getter.get_text('./progress/prog.txt'), getter.get_text('./progress/progmap.txt'), getter.get_plan()) # 本文

        flag = sender.mail_send(subject, body)
        print(flag)

# 毎日20:00にメール送信
def main():
    send_mail()
    # schedule.every(1).day.at('20:00').do(send_mail)
    # while(True):
    #     schedule.run_pending()
    #     time.sleep(30)

if __name__ == '__main__':
    main()
```


機能としては, 「毎日20:00に進捗報告メールを, 指定メールサーバーに対して送信」「毎日12:00にノルマ確認メールを, 指定メールアドレスに対して送信」の2つを実装している.また, 進捗報告メールを送信するのは平日のみであるため, 休日と祝日以外の日のみ進捗報告メールを送信する. しかしノルマ確認メールは毎日送信する必要があったため, 毎日送信するように実装している.   

今回作成したプログラム(auto_mail.py)は, Windows10で動作することを確認済みである. 
