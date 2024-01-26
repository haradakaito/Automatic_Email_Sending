from email import message
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
            ユーザー名(静大メールで登録したMicrosoftアカウント)
        password : str
            パスワード(静大メールで登録したMicrosoftアカウント)
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
        >>> sender = Sender('件名', '本文', '宛先')
        >>> sender.send()
    """

    # クラス変数
    smtp_host = 'smtp-mail.outlook.com'  # SMTPサーバーのホスト名
    smtp_port = 587  # SMTPサーバーのポート番号（Outlookの場合は587）
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