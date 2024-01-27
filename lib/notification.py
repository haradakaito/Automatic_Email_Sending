import requests
import json
import datetime as dt
from pathlib import Path

current_dir = Path(__file__).resolve().parent
conf_path = current_dir / '../config/config.json'

def line_notify(message):
    # 設定ファイルの読み込み
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    line_notify_token = conf['notification']['line_notify_token']
    line_notify_api = conf['notification']['line_notify_api']
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)

def line_notify_daily_report(notify_list):
    message  = f'{dt.date.today()}\n\n'

    message += '進捗報告送信リスト\n'
    message += '-----------------------------\n'

    base_date_time = dt.datetime.combine(dt.date.today(), dt.time(20, 0, 0))
    for i in range(len(notify_list)):
        send_date_time = base_date_time + dt.timedelta(seconds=notify_list[i][1])
        message += f'{notify_list[i][0]}: 送信予定時刻{send_date_time.strftime("%H:%M")}\n'
    message += '-----------------------------'

    line_notify(message)