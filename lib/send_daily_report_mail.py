import json
import time
from pathlib import Path
from mail.contents import Contents
from mail.sender import Sender
from database_loading import GetProperties

# 設定ファイルの読み込み
current_dir = Path(__file__).resolve().parent
conf_path = current_dir / '../config/config.json'
conf = json.load(open(conf_path, 'r', encoding='utf-8'))

def send_daily_report(db_id, sleep_time):

    time.sleep(sleep_time) # sleep_time秒待機
    user_info, _ = GetProperties().get_db_info(db_id=db_id) # db_idからメールを送信
    if not any([p=='' for p in user_info.values()]): # user_infoが全て記入されている
        mail_contents = Contents(**user_info)
        subject = mail_contents.create_subject() # 件名
        body = mail_contents.create_body() # 本文
        to_email = conf['send_daily_report_mail']['to_email']

        # 送信
        sender = Sender(from_email=user_info['email'], to_email=to_email, user_name=user_info['email'], password=user_info['password'], subject=subject, body=body)
        sender.send()