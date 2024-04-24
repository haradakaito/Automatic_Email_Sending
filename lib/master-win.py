import schedule
import random
import time
from threading import Thread
from _schedule import Schedule
from _database_loading import GetProperties
from _notification import line_notify_daily_report
from _send_daily_report_mail import send_daily_report

def main(base_time):
    # 休祝日を除く
    if Schedule().is_today_holiday() == False:
        # 各ユーザーのデータベースIDを取得
        db_id_list = GetProperties().get_dbid_list()
        # 各ユーザーの名前を取得
        user_name_list, flag_list = GetProperties().get_user_name_list(db_id_list)
        # 送信時刻をランダムに設定
        sleep_time_list = [60*abs(random.gauss(25,20)) for _ in range(len(db_id_list))]
        # LineNotifyで日報送信予定時刻を通知
        notify_list = list(zip(user_name_list, sleep_time_list))
        line_notify_daily_report(notify_list, flag_list, base_time)
        # マルチスレッドで全ユーザーの日報を送信
        for db_id, sleep_time in zip(db_id_list, sleep_time_list):
            thread = Thread(target=send_daily_report, args=(db_id, sleep_time))
            thread.start()

if __name__ == '__main__':
    # 毎日19:45にmain関数を実行
    base_time = ['19','45']
    schedule.every(1).day.at(f'{base_time[0]}:{base_time[1]}').do(main, base_time=base_time)
    while(True):
        schedule.run_pending()
        time.sleep(1)