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

# メイン処理
def main() -> None:
    # 事前通知して30分後に送信
    _pre_notify(wait_second=1800)

    # 送信可能なデータベースIDを取得
    checked_dbid    = notiontools.check_all_dbid()
    suitable_dbid   = [dbid for dbid, result in checked_dbid.items() if result]
    all_user_wait = {} # 各ユーザーの送信予定時間を取得
    for dbid in suitable_dbid:
        name = notiontools.get_property(dbid, "苗字")
        wait_second = utils.setting_wait_second()
        all_user_wait[name] = wait_second

    # 各ユーザーのメール送信（並列処理）
    threads = []
    for dbid in suitable_dbid:
        wait_second = all_user_wait[notiontools.get_property(dbid, "苗字")]
        threads.append(Thread(target=_user_process, args=(dbid, wait_second)))
    for t in threads:
        t.start()

    # 送信予定時間を通知
    linenotifytools.notify_send_time(all_user_wait=all_user_wait)

# 事前通知
def _pre_notify(wait_second) -> None:
    checked_user     = notiontools.check_all_user()
    correctable_time = datetime.now() + timedelta(seconds=wait_second)
    linenotifytools.notify_checked_user(checked_user=checked_user, correctable_time=correctable_time)
    time.sleep(wait_second)
    return

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
    body         = contents.create_body(name=name,                 # ユーザー名
                                        grade=grade,               # 学年
                                        progress=progress,         # 進捗項目
                                        progress_map=progress_map, # 進捗マップ
                                        event=event,               # 予定
                                        signature=signature,       # 署名
                                        free=free)                 # 自由記入欄
    # メール送信（wait_second秒だけ待機して送信）
    time.sleep(wait_second)
    mailsender.send_mail(from_addr, subject, body, password)

if __name__ == "__main__":
    if utils.today_is_holiday():
        pass
    # 本日が休祝日でない場合
    else:
        main()