import json
import time
from pathlib import Path
from _contents import Contents
from _sender import Sender
from _database_loading import GetProperties

# 設定ファイルの読み込み
current_dir = Path(__file__).resolve().parent
conf_path = current_dir / '../config/config.json'
conf = json.load(open(conf_path, 'r', encoding='utf-8'))

def send_daily_report(db_id, sleep_time):
    """
        メールで日報を送信する
        
        Parameters
        ---
        db_id : str
            データベースID
        sleep_time : int
            送信時刻までの待機時間（秒）
        
        Returns
        ---
        None
    """

    # sleep_time秒待機
    time.sleep(sleep_time)
    # db_idからメールを送信するユーザー情報を取得
    user_info, _ = GetProperties().get_db_info(db_id=db_id)
    # user_infoが全て記入されている場合のみメール送信
    if not any([p=='' for p in user_info.values()]):
        # メール内容の作成
        mail_contents = Contents(**user_info)
        # 件名と本文の作成
        subject = mail_contents.create_subject()
        # 本文の作成
        body = mail_contents.create_body()
        # 送信先メールアドレス
        to_email = conf['send_daily_report_mail']['to_email']
        # メール送信
        sender = Sender(from_email=user_info['email'], to_email=to_email, user_name=user_info['email'], password=user_info['password'], subject=subject, body=body)
        sender.send()