import schedule
import time

from threading import Thread
from datetime import datetime

from _getutils import Getutils
from _sendutils import Sendutils

def main():
    getutils = Getutils()
    sendutils = Sendutils()
    # 平日のみ実行
    if getutils.today_is_holiday() == False:
        try:
            # 全ユーザーの情報を事前に読み込んでおく
            all_db_info = getutils.get_all_db_info()
            all_user_subject = getutils.get_all_user_subject(all_db_info)
            all_user_event = getutils.get_all_user_event(all_db_info)
            all_user_body = getutils.get_all_user_body(all_db_info, all_user_event)
            
            # 送信時刻を設定し，全員に通知メッセージを送信
            all_send_name = [db_info['name'] for db_info in all_db_info]
            all_sleep_time = getutils.get_sleep_time(len(all_send_name))
            sendutils.send_notify_all(all_send_name, all_sleep_time)
            
            # マルチスレッドでメール送信
            all_send_util = [[db_info['password'], db_info['email']] for db_info in all_db_info]
            threads = []
            for i in range(len(all_db_info)):
                thread = Thread(target=sendutils.send_mail, args=(all_send_util[i], all_user_subject[i], all_user_body[i], all_sleep_time[i]))
                threads.append(thread)
            for t in threads:
                t.start()
        except:
            error_time = datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} ERROR')

if __name__ == '__main__':
    # 毎日19:45にmain関数を実行
    base_time = ['19','45']
    schedule.every(1).day.at(f'{base_time[0]}:{base_time[1]}').do(main)
    while(True):
        schedule.run_pending()
        time.sleep(1)
