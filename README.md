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
```python
class Getter:

    # 進捗文を読み込む
    def get_text(self, path:str):
        self.text_list = []
        with open(path, 'r', encoding='UTF-8') as self.f:
            for self.line in self.f:
                self.text_list.append(self.line.split("\n")[0])

        return self.text_list

    # 予定を作成
    def get_plan(self):
        self.today = datetime.date.today()
        self.weekday = self.today.weekday()

        # GMは(月曜日)，WRは(水曜日)
        self.gm_delta = 7 - self.weekday
        if self.weekday >= 2:
            self.wr_delta = 9 - self.weekday
        else: self.wr_delta = 2 - self.weekday
        self.gm, self.wr = self.today + datetime.timedelta(self.gm_delta), self.today + datetime.timedelta(self.wr_delta)

        self.gm = f'{self.gm.year}/{str(self.gm.month).zfill(2)}/{str(self.gm.day).zfill(2)}'
        self.wr = f'{self.wr.year}/{str(self.wr.month).zfill(2)}/{str(self.wr.day).zfill(2)}'

        self.plan = []
        self.plan.append(f'{self.gm} GM')
        self.plan.append(f'{self.wr} WR')

        return self.plan
```

機能としては, 「毎日20:00に進捗報告メールを, 指定メールサーバーに対して送信」「毎日12:00にノルマ確認メールを, 指定メールアドレスに対して送信」の2つを実装している.また, 進捗報告メールを送信するのは平日のみであるため, 休日と祝日以外の日のみ進捗報告メールを送信する. しかしノルマ確認メールは毎日送信する必要があったため, 毎日送信するように実装している.   

今回作成したプログラム(auto_mail.py)は, Windows10で動作することを確認済みである. 
