from lib.mail.contents import Contents
from lib.mail.sender import Sender

def send_daily_report():
    # メール用の宛先情報
    from_email = 'shimada.takuto.21@shizuoka.ac.jp'  # 送信元メールアドレス
    to_email = 'shimada.takuto.21@shizuoka.ac.jp'  # 送信先メールアドレス
    # メールアカウント情報
    user_name = 'shimada.takuto.21@shizuoka.ac.jp'  # ユーザー名(静大メールで登録したMicrosoftアカウント)
    password = '#######'  # パスワード(静大メールで登録したMicrosoftアカウント)
    # メール内容
    mail_contents = Contents(user_name='島田', user_grade='M1')
    subject = mail_contents.create_subject() # 件名
    body = mail_contents.create_body() # 本文
    # 送信
    sender = Sender(from_email=from_email, to_email=to_email, user_name=user_name, password=password, subject=subject, body=body)
    sender.send()

if __name__ == '__main__':
    send_daily_report()