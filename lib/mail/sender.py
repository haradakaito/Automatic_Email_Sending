from email import message
import json
from pathlib import Path
import smtplib

class Sender:
    """
        MailSender
        ===
        outlookを用いてメールを送信する
        
        Parameters
        ---
        from_email : str
            送信元
        to_email : str
            宛先
        user_name : str
            ユーザー名(Microsoftアカウント)
        password : str
            パスワード(Microsoftアカウント)
        subject : str
            件名
        body : str
            本文
        
        Methods
        ---
        send(subject, body, to)
            メールを送信する
        
        Usage
        ---
        >>> sender = Sender(from_email, to_email, user_name, password, subject, body)
        >>> sender.send()
    """

    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../../config/config.json'
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    # クラス変数
    smtp_host = conf['sender']['smtp_host']  # SMTPサーバーのホスト名
    smtp_port = conf['sender']['smtp_port']  # SMTPサーバーのポート番号（Outlookの場合は587）
    def __init__(self, from_email, to_email, user_name, password, subject, body):
        self.from_email = from_email  # 送信元メールアドレス
        self.to_email = to_email  # 送信先メールアドレス
        self.user_name = user_name  # ユーザー名
        self.password = password  # パスワード
        self.subject = subject  # 件名
        self.body = body  # 本文

    def send(self):
        #メッセージ内容
        msg = message.EmailMessage()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = self.subject
        msg.set_content(self.body)
        # サーバーとのやりとり
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.user_name,self.password)
        server.send_message(msg)
        server.quit()