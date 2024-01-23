# ライブラリのインポート
import jpholiday
import datetime
import schedule
import time
from mail_package.getter_creator import Getter, Creator, Sender

########################################
# pip install pywin32 schedule jpholiday
########################################

# 休祝日判定(休祝日: True)
def judge_holiday():
    if (jpholiday.is_holiday(datetime.date.today()) == True) or (datetime.datetime.now().weekday() == 5) or (datetime.datetime.now().weekday() == 6):
        return True
    else: return False

# メール送信(休祝日以外)
def send_mail():
    if judge_holiday() == False:

        getter, creator, sender = Getter(), Creator(), Sender()

        subject =  creator.create_subject() # 件名
        body = creator.create_body(getter.get_text('./progress/prog.txt'), getter.get_text('./progress/progmap.txt'), getter.get_plan()) # 本文

        flag = sender.mail_send(subject, body)
        print(flag)

# 毎日20:00にメール送信
def main():
    schedule.every(1).day.at('20:00').do(send_mail)
    while(True):
        schedule.run_pending()
        time.sleep(30)

if __name__ == '__main__':
    main()