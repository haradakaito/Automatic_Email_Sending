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

def main() -> None:
    # 送信可能な[ユーザー名, 可/否，データベースID]を取得
    check_result = notiontools.check_all_user()
    all_username = [username for username, result, _    in check_result if result]
    all_dbid     = [dbid     for _       , result, dbid in check_result if result]
    # 各ユーザーの送信予定時間を取得
    all_wait_second = utils.setting_wait_second(num=len(all_username))
    # 各ユーザーのメール送信（並列処理）
    threads = []
    for username, dbid, wait_second in zip(all_username, all_dbid, all_wait_second):
        threads.append(Thread(target=_user_process, args=(username, dbid, wait_second)))
    for t in threads:
        t.start()
    # 送信予定時間を通知
    linenotifytools.notify_sendtime(all_username=all_username, all_wait_second=all_wait_second)

def _user_process(username:str, dbid:str, wait_second:int) -> None:
    # ユーザー情報を取得
    grade        = notiontools.get_property(dbid, "学年")
    from_addr    = notiontools.get_property(dbid, "静大メール")
    password     = notiontools.get_property(dbid, "パスワード")
    progress     = notiontools.get_property(dbid, "進捗項目")
    progress_map = notiontools.get_property(dbid, "進捗マップ")
    event        = googlecalendartools.get_event(username)
    signature    = notiontools.get_property(dbid, "署名")
    free         = notiontools.get_property(dbid, "自由記入欄")
    # 件名と本文を作成
    subject = contents.create_subject()
    body    = contents.create_body(username, grade, progress, progress_map, event, signature, free)
    # メール送信
    time.sleep(wait_second)
    mailsender.send_mail(from_addr, subject, body, password)

def pre_notify(wait_second) -> None:
    # 送信可能な[ユーザー名, 可/否，データベースID]を取得
    check_result = notiontools.check_all_user()
    linenotifytools.notify_check_result(check_result=check_result, 
                                        correctable_time=datetime.now()+timedelta(seconds=wait_second))
    time.sleep(wait_second)
    return

if __name__ == "__main__":
    if utils.today_is_holiday():
        pass
    # 本日が休祝日でない場合
    else:
        # 事前通知して30分後に送信
        pre_notify(wait_second=1800)
        # 送信可能なユーザーのみ送信
        main()