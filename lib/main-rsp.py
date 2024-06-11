from threading import Thread

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
        all_subject             = getutils.get_all_user_subject(all_db_info)    # 件名
        all_body                = getutils.get_all_user_body(all_db_info)       # 本文
        all_password, all_email = getutils.get_pass_email(all_db_info)          # パスワードとメールアドレス
        all_sleeptime           = getutils.get_all_sleeptime(all_db_info)       # 送信時刻

        # 全員に通知メッセージを送信
        sendutils.send_notify_all(all_sleeptime)

        # マルチスレッドでメール送信
        threads = []
        for i in range(len(all_email)):
            thread = Thread(
                target = sendutils.send_mail,
                args = (
                    all_password[i],    # パスワード
                    all_email[i],       # メールアドレス
                    all_subject[i],     # 件名
                    all_body[i],        # 本文
                    all_sleeptime[i][2] # 送信時刻（秒数）
                    )
                )
            threads.append(thread)
        for t in threads:
            t.start()

if __name__ == '__main__':
    # 全員のデータベースのプロパティ情報を取得
    all_db_info = getutils.get_all_db_info()
    main(all_db_info)