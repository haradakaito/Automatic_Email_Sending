# ライブラリのインポート
import win32com.client
import datetime
import math
import os
import jpholiday
import time
import schedule
from plyer import notification
from playsound import playsound
from dateutil.relativedelta import relativedelta

# 日付取得
def get_today():
    today = ""
    month_ini = ""
    day_ini = ""

    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day

    if int(math.log10(month)) == 0:
        month_ini = "0"
    if int(math.log10(day)) == 0:
        day_ini = "0"

    today = "("+str(year)+"/"+month_ini+str(month)+"/"+day_ini+str(day)+")"

    return today

def create_progress_map():
    tmp = []
    progress_map = ""
    with open('./progress/progress_map.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            add_text = line.split("\n")[0]
            tmp.append(add_text)

    for a in tmp:
        progress_map += "\n"+a

    return progress_map

# 予定を作成
def create_progress_plan():
    plan = []
    today = datetime.date.today()
    gm = 7 - today.weekday()
    if today.weekday() >= 2:
        wr = 9 - today.weekday()
    elif today.weekday() < 2:
        wr = 2 - today.weekday()

    gm = today + datetime.timedelta(days=gm)
    wr = today + datetime.timedelta(days=wr)

    gm_month_ini = gm_day_ini = wr_month_ini = wr_day_ini = ""
    if int(math.log10(gm.month)) == 0:
        gm_month_ini = "0"
    if int(math.log10(gm.day)) == 0:
        gm_day_ini = "0"
    if int(math.log10(wr.month)) == 0:
        wr_month_ini = "0"
    if int(math.log10(wr.day)) == 0:
        wr_day_ini = "0"

    gm = str(gm.year)+"/"+gm_month_ini+str(gm.month)+"/"+gm_day_ini+str(gm.day)
    wr = str(wr.year)+"/"+wr_month_ini+str(wr.month)+"/"+wr_day_ini+str(wr.day)

    plan.append(str(gm)+" GM")
    plan.append(str(wr)+" WR")

    return plan

# 本文を作成
def create_progress_body(contents, plan):

    head = "agri-minenoの皆様\n峰野研究室B4の原田です. 本日の進捗を共有させていただきます.\n"
    head += "\n本日は,"
    for a in contents:
        head += "「"+a+"」"
    head += "を行いました."

    text = create_progress_map()

    hoot = "\n-----今後の予定・その他-----"
    for a in plan:
        hoot += "\n"+a
    hoot += "\n-------------------------------"
    hoot += "\n静岡大学情報学部情報科学科4年\n原田海斗\nharada.kaito.20@shizuoka.ac.jp"
    hoot += "\n-------------------------------"

    mail_text = head+"\n"+text+"\n"+hoot

    return mail_text

# 土日祝判定
def judge_holiday():
    if (jpholiday.is_holiday(datetime.date.today()) == True) or (datetime.datetime.now().weekday() == 5) or (datetime.datetime.now().weekday() == 6):
        return True
    else:
        return False

# 内容を作成
def create_contents():

    contents = []
    with open('./progress/progress.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            contents.append(line.split("\n")[0])

    return contents

# 進捗メール送信
def send_progress_mail():

    if judge_holiday() == False:
        mail_title = "本日の進捗について" + get_today()
        contents = create_contents()
        plan = create_progress_plan()
        mail_text = create_progress_body(contents, plan)

        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = "progress@minelab.jp"
        mail.BCC = "mkr.k117@gmail.com"
        mail.Subject = mail_title
        mail.Body = mail_text
        #mail.Display(True)
        mail.Send()

# ノルマ確認メール送信
def send_quota_mail():

    mail_title = "本日のノルマ確認" + get_today()
    mail_text = "本日のノルマ確認時刻になりました. (送信専用メールのため, 返信不要)"
    mail_text += "\nまだノルマを達成していない場合は, 本日中に必ずノルマを達成してください."

    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.To = "kousukesakai0201@gmail.com"
    mail.BCC = "mkr.k117@gmail.com"
    mail.Subject = mail_title
    mail.Body = mail_text
    #mail.Display(True)
    mail.Send()

# 12:00「ノルマ確認メール」, 20:00「進捗メール」
schedule.every(1).day.at("12:00").do(send_quota_mail)
schedule.every(1).day.at("20:00").do(send_progress_mail)
while(True):
    schedule.run_pending()
    time.sleep(1)