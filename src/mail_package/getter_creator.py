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

        # MeetingAは(月曜日)，MeetingBは(水曜日)
        self.mtg_A_delta = 7 - self.weekday
        if self.weekday >= 2:
            self.mtg_B_delta = 9 - self.weekday
        else: self.mtg_B_delta = 2 - self.weekday
        self.mtg_A, self.mtg_B = self.today + datetime.timedelta(self.mtg_A_delta), self.today + datetime.timedelta(self.mtg_B_delta)

        self.mtg_A = f'{self.mtg_A.year}/{str(self.mtg_A.month).zfill(2)}/{str(self.mtg_A.day).zfill(2)}'
        self.mtg_B = f'{self.mtg_B.year}/{str(self.mtg_B.month).zfill(2)}/{str(self.mtg_B.day).zfill(2)}'

        self.plan = []
        self.plan.append(f'{self.mtg_A} mtg_A')
        self.plan.append(f'{self.mtg_B} mtg_B')

        return self.plan


# 作成関係
class Creator:

    # メール件名作成
    def create_subject(self):
        self.subject = ''

        self.today = datetime.date.today()
        self.year, self.month, self.day = str(self.today.year), str(self.today.month).zfill(2), str(self.today.day).zfill(2)

        self.subject += '本日のメールについて'
        self.subject += f'({self.year}/{self.month}/{self.day})'

        return self.subject

    # 本文作成
    def create_body(self, prog_list:list, progmap_list:list, plan_list:list):
        self.head, self.text, self.hoot = '', '', ''

        # ヘッダー
        self.head += '\n本日は,'
        for self.prog in prog_list: self.head += f'「{self.prog}」'
        self.head += 'を行いました.'

        # 本文
        for self.progmap in progmap_list: self.text += f'\n{self.progmap}'

        # フッター
        self.hoot = '\n-----今後の予定・その他-----'
        for self.plan in plan_list: self.hoot += f'\n{self.plan}'
        self.hoot += '\n-------------------------------'

        self.body = self.head+'\n'+self.text+'\n'+self.hoot

        return self.body

# 送信関係
class Sender:

    # メール送信
    def mail_send(self, subject, body):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.mail = self.outlook.CreateItem(0)
        self.mail.To = "XXX@XXX"
        self.mail.Subject = subject
        self.mail.Body = body
        self.mail.Send()

        return True
