import json
import requests
import smtplib
import time
from datetime import datetime, timedelta
from email import message
from pathlib import Path

class Sender:

    """
        通知を送信するクラス

        Parameters
        ----------
        None

        Attributes
        ----------
        LINE_NOTIFY_TOKEN : str
            LINE Notifyのトークン

        LINE_NOTIFY_API : str
            LINE NotifyのAPI

        SMTP_HOST : str
            SMTPのホスト名

        SMTP_PORT : int
            SMTPのポート番号

        TO_EMAIL : str
            送信先メールアドレス

        Methods
        -------
        send_notify_all(all_user_name:list, all_sleep_time:list)
            全員に通知を送信

        _send_notify(message)
            通知を送信

        send_mail(send_util, subject, body, sleep_time)
            メールを送信
    """

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../config/config.json'
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    # クラス変数
    LINE_NOTIFY_TOKEN = conf['notification']['LINE_NOTIFY_TOKEN']
    LINE_NOTIFY_API = conf['notification']['LINE_NOTIFY_API']
    SMTP_HOST = conf['sender']['SMTP_HOST']
    SMTP_PORT = conf['sender']['SMTP_PORT']
    TO_EMAIL = conf['send_daily_report_mail']['TO_EMAIL']

    # 全員に通知
    def send_notify_all(self, all_user_name:list, all_sleep_time:list):
        """
            全員に通知を送信

            Parameters
            ----------
            all_user_name : list
                全ユーザーの名前

            all_sleep_time : list
                全ユーザーの送信時刻

            Returns
            -------
            None

            Notes
            -----
            通知のメッセージ例:
            2024/04/26

            進捗報告送信リスト
            -----------------------------

            user1: 送信予定時刻21:00
            user2: 送信予定時刻20:30
            user3: 送信予定時刻20:10
            user4: 送信予定時刻19:55
            user5: 送信予定時刻20:00

            -----------------------------
        """
        message  = f'{datetime.today().strftime('%Y/%m/%d')}\n\n'
        message += '進捗報告送信リスト\n'
        message += '-----------------------------\n'
        for user_name, sleep_time in zip(all_user_name, all_sleep_time):
            send_time = datetime.now() + timedelta(seconds=sleep_time+60)
            message += f'{user_name}: 送信予定時刻{send_time.strftime("%H:%M")}\n'
        message += '-----------------------------'
        self._send_notify(message)

    def _send_notify(self, message):
        self.payload = {'message': message}
        self.headers = {'Authorization': 'Bearer ' + self.LINE_NOTIFY_TOKEN}
        requests.post(self.LINE_NOTIFY_API, data=self.payload, headers=self.headers)

    # メール送信
    def send_mail(self, send_util:list, subject:str, body:str, sleep_time:int):
        """
            メールを送信

            Parameters
            ----------
            send_util : list
                メールアドレスとパスワード

            subject : str
                件名

            body : str
                本文

            sleep_time : int
                待ち時間

            Returns
            -------
            None
        """
        password, email = send_util[0], send_util[1]

        msg = message.EmailMessage()
        msg['From'] = email
        msg['To'] = self.TO_EMAIL
        msg['Subject'] = subject
        msg.set_content(body)
        
        # 待ち時間
        time.sleep(sleep_time)

        server = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(password=password, user=email)
        server.send_message(msg)
        server.quit()