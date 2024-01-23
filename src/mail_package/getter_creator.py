import datetime
import win32com.client

# 取得関係
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


# 作成関係
class Creator:

    # メール件名作成
    def create_subject(self):
        self.subject = ''

        self.today = datetime.date.today()
        self.year, self.month, self.day = str(self.today.year), str(self.today.month).zfill(2), str(self.today.day).zfill(2)

        self.subject += '本日の進捗について'
        self.subject += f'({self.year}/{self.month}/{self.day})'

        return self.subject

    # 本文作成
    def create_body(self, prog_list:list, progmap_list:list, plan_list:list):
        self.head, self.text, self.hoot = '', '', ''

        # ヘッダー
        self.head = '峰野研究室の皆様\n峰野研究室B4の原田です.本日の進捗を共有させていただきます.\n'
        self.head += '\n本日は,'
        for self.prog in prog_list: self.head += f'「{self.prog}」'
        self.head += 'を行いました.'

        # 本文
        for self.progmap in progmap_list: self.text += f'\n{self.progmap}'

        # フッター
        self.hoot = '\n-----今後の予定・その他-----'
        for self.plan in plan_list: self.hoot += f'\n{self.plan}'
        self.hoot += '\n-------------------------------'
        self.hoot += '\n静岡大学情報学部情報科学科4年\n原田海斗\nharada.kaito.20@shizuoka.ac.jp'
        self.hoot += '\n-------------------------------'

        self.body = self.head+'\n'+self.text+'\n'+self.hoot

        return self.body

# 送信関係
class Sender:

    # メール送信
    def mail_send(self, subject, body):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.mail = self.outlook.CreateItem(0)
        self.mail.To = "mkr.k117@gmail.com"
        self.mail.Subject = subject
        self.mail.Body = body
        # self.mail.Display(True)
        self.mail.Send()

        return True
