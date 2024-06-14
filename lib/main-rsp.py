import time

from threading import Thread
from datetime  import datetime, timedelta

from _notiontools         import Notiontools
from _linenotifytools     import Linenotifytools
from _utils               import Utils
from _mailsender          import Mailsender
from _googlecalendartools import GoogleCalendarTools
from _contents            import Contents

notiontools         = Notiontools()
linenotifytools     = Linenotifytools()
utils               = Utils()
mailsender          = Mailsender()
googlecalendartools = GoogleCalendarTools()
contents            = Contents()

# 送信結果を保存する辞書
send_results = {}

# メイン処理
def main() -> None:
    # 事前通知して30分後に送信
    _pre_notify(wait_second=1800)

    # データベースIDを取得
    checked_dbid = notiontools.check_all_dbid()
    # 各ユーザーごとにメール送信実行（並列処理）
    threads = []
    all_user_wait = {}
    for dbid, result in checked_dbid.items():
        # 送信可能な場合
        if result:
            # 待機時間を取得
            wait_second         = utils.setting_wait_second()
            # ユーザー名と待機時間を辞書に保存
            name                = notiontools.get_property(dbid, "苗字")
            all_user_wait[name] = wait_second
            # スレッドで実行（入力：データベースID，待機時間）
            thread = Thread(target=_user_process, args=(dbid, wait_second))
            threads.append(thread)
            thread.start()

    # 送信予定時間を通知
    linenotifytools.notify_send_time(all_user_wait=all_user_wait)

    # スレッドの終了を待機
    for thread in threads:
        thread.join()
    # 送信結果を通知
    linenotifytools.notify_send_result(send_results=send_results)

# 事前通知
def _pre_notify(wait_second) -> None:
    checked_user     = notiontools.check_all_user()
    correctable_time = datetime.now() + timedelta(seconds=wait_second)
    linenotifytools.notify_checked_user(checked_user=checked_user, correctable_time=correctable_time)
    # time.sleep(wait_second)

# ユーザーごとの処理
def _user_process(dbid:str, wait_second:int) -> None:
    # ユーザー情報を取得
    name         = notiontools.get_property(dbid, "苗字")
    grade        = notiontools.get_property(dbid, "学年")
    from_addr    = notiontools.get_property(dbid, "静大メール")
    password     = notiontools.get_property(dbid, "パスワード")
    progress     = notiontools.get_property(dbid, "進捗項目")
    progress_map = notiontools.get_property(dbid, "進捗マップ")
    signature    = notiontools.get_property(dbid, "署名")
    free         = notiontools.get_property(dbid, "自由記入欄")
    event        = googlecalendartools.get_event(name=name)
    
    # 件名と本文を作成
    subject      = contents.create_subject()
    body         = contents.create_body(
        name         = name,
        grade        = grade,
        progress     = progress,
        progress_map = progress_map,
        event        = event,
        signature    = signature,
        free         = free
        )
    # メール送信（wait_second秒だけ待機して送信）
    # time.sleep(wait_second)
    send_result = mailsender.send_mail(
        from_addr = from_addr,
        subject   = subject,
        body      = body,
        password  = password
        )
    # 送信結果を保存
    send_results[name] = send_result

if __name__ == "__main__":
    if utils.today_is_holiday():
        pass
    # 本日が休祝日でない場合
    else:
        main()