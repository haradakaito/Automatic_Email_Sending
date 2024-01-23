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
## メインプログラム
```python
# 休祝日判定(休祝日: True)
def judge_holiday():
    ## 土日祝の場合 -> True ##

# メール送信(休祝日以外)
def send_mail():

    if judge_holiday() == False:
        getter, creator, sender = Getter(), Creator(), Sender()

        ## 件名と本文を取得 ##
        ## メール送信 ##

# メイン文
def main():
    ## 毎日20:00にsend_mail()を実行 ##

if __name__ == '__main__':
    main()
```
※作成したプログラム(auto_mail.py)は, Windows10で動作することを確認済みである. 
