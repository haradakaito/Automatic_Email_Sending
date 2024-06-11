from threading import Thread

from _getutils import Getutils
from _sendutils import Sendutils

def main():
    """
        メイン関数

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    getutils = Getutils()
    sendutils = Sendutils()

    # 全員のデータベースをプリローディング
    all_db_info = getutils.get_all_db_info() # 全員のデータベースIDを取得
    all_user_subject = getutils.get_all_user_subject(all_db_info) # 全員の件名を取得
    all_user_event = getutils.get_all_user_event(all_db_info) # 全員の予定を取得
    all_user_body = getutils.get_all_user_body(all_db_info, all_user_event) # 全員の本文を取得

    # 送信時刻を設定
    all_sleep_time = getutils.get_sleep_time(len(all_db_info))
    # 全員に通知メッセージを送信
    all_send_name = [db_info['name'] for db_info in all_db_info]
    sendutils.send_notify_all(all_send_name, all_sleep_time)

    # マルチスレッドでメール送信
    all_send_util = [[db_info['password'], db_info['email']] for db_info in all_db_info]
    threads = []
    for i in range(len(all_db_info)):
        thread = Thread(target=sendutils.send_mail, args=(all_send_util[i], all_user_subject[i], all_user_body[i], all_sleep_time[i]))
        threads.append(thread)
    for t in threads:
        t.start()

if __name__ == '__main__':
    main()