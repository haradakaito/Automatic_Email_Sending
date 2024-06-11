import time
import schedule

from threading import Thread

from _notiontools        import Notiontools
from _linenotifytools    import Linenotifytools
from _utils              import Utils
from _mailsender         import Mailsender
from _goolecalendartools import GoogleCalendarTools
from _contents           import Contents

notiontools         = Notiontools()
linenotifytools     = Linenotifytools()
utils               = Utils()
mailsender          = Mailsender()
googlecalendartools = GoogleCalendarTools()
contents            = Contents()

# 全ユーザーの送信可否を通知
def pre_notify():
    check_result = notiontools.check_all_user()
    linenotifytools.notify_check_result(check_result=check_result)

def main():
    # 本日が休祝日であれば何もしない
    if utils.today_is_holiday():
        pass
    else:
        # 送信可能なユーザー名を取得
        check_result = notiontools.check_all_user()
        all_username = [username for username, result, _    in check_result if result]
        all_dbid     = [dbid     for _       , result, dbid in check_result if result]
        all_waittime = utils.setting_waittime(num=len(all_username))

        # マルチスレッドでメール送信
        threads = []
        for username, dbid, waittime in zip(all_username, all_dbid, all_waittime):
            threads.append(Thread(target=_user_process, args=(username, dbid, waittime)))
        for t in threads:
            t.start()

        # 送信予定時間を通知
        linenotifytools.notify_sendtime(all_username=all_username, all_waittime=all_waittime)

def _user_process(username:str, dbid:str, waittime:int) -> None:
    # ユーザー情報を取得
    grade        = notiontools.get_property(dbid, '学年')
    from_addr    = notiontools.get_property(dbid, '静大メール')
    password     = notiontools.get_property(dbid, 'パスワード')
    progress     = notiontools.get_property(dbid, '進捗項目')
    progress_map = notiontools.get_property(dbid, '進捗マップ')
    event        = googlecalendartools.get_event(username)
    signature    = notiontools.get_property(dbid, '署名')
    free         = notiontools.get_property(dbid, '自由記入欄')
    # 件名と本文を作成
    subject = contents.create_subject()
    body    = contents.create_body(username, grade, progress, progress_map, event, signature, free)
    # メール送信
    time.sleep(waittime)
    mailsender.send_mail(from_addr, subject, body, password)

if __name__ == '__main__':
    # 毎日19:00に通知送信，毎日19:30にmain関数を実行
    prenotify_time = ['19','00']
    main_time = ['19','30']
    schedule.every(1).day.at(f'{prenotify_time[0]}:{prenotify_time[1]}').do(pre_notify)
    schedule.every(1).day.at(f'{main_time[0]}:{main_time[1]}').do(main)
    while(True):
        schedule.run_pending()
        time.sleep(1)
