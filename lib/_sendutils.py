import json
import requests
import smtplib
import time
from datetime import datetime, timedelta
from email import message
from pathlib import Path

class Sendutils:

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
    TEST_LINE_NOTIFY_TOKEN = conf['notification']['TEST_LINE_NOTIFY_TOKEN'] # テスト用
    LINE_NOTIFY_API = conf['notification']['LINE_NOTIFY_API']
    SMTP_HOST = conf['sender']['SMTP_HOST']
    SMTP_PORT = conf['sender']['SMTP_PORT']
    TO_EMAIL = conf['send_daily_report_mail']['TO_EMAIL']

    # 全員に通知
    def send_notify_all(self, all_sleeptime:list) -> None:
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


        """
        message  = f'{datetime.today().strftime('%Y/%m/%d')}\n\n'
        message += '進捗報告送信予定時刻\n'
        message += '-----------------------------\n'
        for name, flag, sleeptime in sorted(all_sleeptime, key=lambda x: x[2]): # 送信時刻順にソート（昇順）
            send_time = datetime.now() + timedelta(seconds=sleeptime)
            if flag == True:
                message += f'{name}: {send_time.strftime("%H:%M")}\n'
            else:
                message += f'{name}: ×\n'
        message += '-----------------------------'
        self._send_notify(message)

    def _send_notify(self, message):
        self.payload = {'message': message}
        # self.headers = {'Authorization': 'Bearer ' + self.LINE_NOTIFY_TOKEN}
        self.headers = {'Authorization': 'Bearer ' + self.TEST_LINE_NOTIFY_TOKEN} # テスト用
        requests.post(self.LINE_NOTIFY_API, data=self.payload, headers=self.headers)

    # メール送信
    def send_mail(self, password:str, email:str, subject:str, body:str, sleep_time:int):
        """
            メールを送信

            Parameters
            ----------
            password : str
                パスワード

            email : str
                メールアドレス

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
        server.ehlo()
        server.login(password, email)
        server.send_message(msg)
        server.quit()