from threading import Thread
from datetime import datetime

from _getutils import Getutils
from _sendutils import Sendutils

# インスタンス生成
getutils  = Getutils()
sendutils = Sendutils()

def main(all_db_info:list) -> None:
    """
        メイン関数

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    # 平日のみ実行
    if getutils.today_is_holiday() == False:
        # 全員のメール送信情報を取得
        all_subject             = getutils.get_all_user_subject(all_db_info)         # 件名
        all_event               = getutils.get_all_user_event(all_db_info)           # 予定
        all_body                = getutils.get_all_user_body(all_db_info, all_event) # 本文
        all_password, all_email = getutils.get_pass_email(all_db_info)               # パスワードとメールアドレス

        # 全員に通知メッセージを送信
        all_sleeptime = getutils.get_all_sleeptime(all_db_info)
        sendutils.send_notify_all(all_sleeptime)

        # マルチスレッドでメール送信
        threads = []
        for i in range(len(all_email)):
            thread = Thread(
                target = sendutils.send_mail,
                args = (
                    all_password[i],
                    all_email[i],
                    all_subject[i],
                    all_body[i],
                    all_sleeptime[i][2]
                    )
                )
            threads.append(thread)
        for t in threads:
            t.start()

if __name__ == '__main__':
    # 全員のデータベースのプロパティ情報を取得
    all_db_info = getutils.get_all_db_info()
    main(all_db_info)