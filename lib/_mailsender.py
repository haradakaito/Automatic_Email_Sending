import json
import smtplib

from pathlib import Path
from email   import message

class Mailsender:

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    conf        = json.load(open(conf_path, 'r', encoding='utf-8'))
    # クラス変数
    SMTP_HOST = conf['sender']['SMTP_HOST']
    SMTP_PORT = conf['sender']['SMTP_PORT']
    TO_EMAIL  = conf['send_daily_report_mail']['TO_EMAIL']

    def send_mail(self, from_addr:str, subject:str, body:str, password:str) -> None:
        msg            = message.EmailMessage()
        msg['From']    = from_addr
        msg['To']      = self.TO_EMAIL
        msg['Subject'] = subject
        msg.set_content(body)

        server = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
        # TLS通信を確立する際に自動でechoされるので明示的に書く必要はない（むしろ書くとエラーになる）
        server.starttls()
        server.login(user=from_addr, password=password)
        server.send_message(msg)
        server.quit()