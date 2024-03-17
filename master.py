import schedule
import random
import os
import time
import shutil
from threading import Thread
from lib.schedule import Schedule
from lib.database_loading import GetProperties
from lib.notification import line_notify_daily_report
from lib.send_daily_report_mail import send_daily_report

def send_daily_report_all(base_time):
    # if Schedule().is_today_holiday() == False: # 休祝日を除いて送信

    db_id_list = GetProperties().get_dbid_list()  # 各ユーザーのデータベースIDを取得
    user_name_list, flag_list = GetProperties().get_user_name_list(db_id_list)  # 各ユーザーの名前を取得

    # sleep_time_list = [60*abs(random.gauss(25,20)) for _ in range(len(db_id_list))]  # 送信時刻をランダムに設定
    sleep_time_list = [0 for _ in range(len(db_id_list))]

    notify_list = list(zip(user_name_list, sleep_time_list))
    line_notify_daily_report(notify_list, flag_list, base_time) # LineNotifyで日報送信予定時刻を通知

    # 並列処理で日報送信
    thread_list = []
    for db_id, sleep_time in zip(db_id_list, sleep_time_list):
        thread = Thread(target=send_daily_report, args=(db_id, sleep_time))
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

if __name__ == '__main__':
    send_daily_report_all(base_time=['19','45'])