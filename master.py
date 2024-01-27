import schedule
import random
import time
from threading import Thread
from lib.database_loading import GetProperties
from lib.notification import line_notify_daily_report
from lib.send_daily_report_mail import send_daily_report

def send_daily_report_all():
    db_id_list = GetProperties().get_dbid_list()  # 各ユーザーのデータベースIDを取得
    user_name_list = GetProperties().get_user_name_list(db_id_list)  # 各ユーザーの名前を取得
    sleep_time_list = [random.randint(0, 60*60) for i in range(len(db_id_list))]  # 送信時刻をランダムに設定
    # LineNotifyで日報送信予定時刻を通知
    notify_list = list(zip(user_name_list, sleep_time_list))
    line_notify_daily_report(notify_list)  
    # 並列処理で日報送信
    for db_id, sleep_time in zip(db_id_list, sleep_time_list):
        Thread(target=send_daily_report, args=(db_id, sleep_time)).start()


# 20:00に定期実行
def main():
    schedule.every(1).day.at('20:00').do(send_daily_report_all)
    while(True):
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()