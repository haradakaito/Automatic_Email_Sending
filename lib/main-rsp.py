from threading import Thread
from datetime import datetime

from _getter import Getter
from _sender import Sender

def main():
    """
        メイン関数

        Parameters
        ----------
        None

        Returns
        -------
        True
    """
    getter = Getter()
    sender = Sender()
    # 平日のみ実行
    if getter.today_is_holiday() == False:
        # 全員のデータベースID
        all_db_info = getter.get_all_db_info()
        # 全員の件名
        all_user_subject = getter.all_get_user_subject(all_db_info)
        # 全員の予定
        all_user_event = getter.get_all_user_event(all_db_info)
        # 全員の本文
        all_user_body = getter.get_all_user_body(all_db_info, all_user_event)
        # 送信時刻を設定
        all_sleep_time = getter.get_sleep_time(len(all_db_info))
        # 全員に通知メッセージを送信
        all_send_name = [db_info['name'] for db_info in all_db_info]
        sender.send_notify_all(all_send_name, all_sleep_time)
        # マルチスレッドでメール送信
        all_send_util = [[db_info['password'], db_info['email']] for db_info in all_db_info]
        threads = []
        for i in range(len(all_db_info)):
            thread = Thread(target=sender.send_mail, args=(all_send_util[i], all_user_subject[i], all_user_body[i], all_sleep_time[i]))
            threads.append(thread)
        # 全スレッド同時実行
        for t in threads:
            t.start()
    return True

if __name__ == '__main__':
    result = main()
    if result != True:
        error_time = datetime.now().strftime('[%Y/%m/%d] %H:%M')
        print(f'{error_time} ERROR')