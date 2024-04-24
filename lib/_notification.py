import requests
import json
import datetime as dt
from pathlib import Path

class Notification:
    """
        Notification
        ===
        LINENotifyを用いてユーザーに通知する
        
        Parameters
        ---
        None
        
        Methods
        ---
        line_notify_daily_report(notify_list, flag_list, base_time)
            進捗報告送信予定時間を通知する
    """

    def __init__(self):
        # 設定ファイルの読み込み
        self.current_dir = Path(__file__).resolve().parent
        self.conf_path = self.current_dir / '../config/config.json'
        self.conf = json.load(open(self.conf_path, 'r', encoding='utf-8'))
        
    def line_notify_daily_report(self, notify_list, flag_list, base_time):
        """
            LINENotifyを用いてユーザーに通知する
            
            Parameters
            ---
            notify_list : list
                通知リスト
            flag_list : list
                通知可能フラグリスト
            base_time : list
                進捗報告送信予定時間の基準時刻
            
            Returns
            ---
            None
        """
        message  = f'{dt.date.today()}\n\n'
        message += '進捗報告送信リスト\n'
        message += '-----------------------------\n'
        base_date_time = dt.datetime.combine(dt.date.today(), dt.time(int(base_time[0]), int(base_time[1]), 0))
        for i in range(len(notify_list)):
            send_date_time = base_date_time + dt.timedelta(seconds=int(notify_list[i][1]))
            if flag_list[i] == True:
                message += f'{notify_list[i][0]}: 送信予定時刻{send_date_time.strftime("%H:%M")}\n'
            else:
                message += f'{notify_list[i][0]}: × (修正可能時刻～{send_date_time.strftime("%H:%M")})\n'
        message += '-----------------------------'
        self._line_notify(message)

    def _line_notify(self, message):
        self.line_notify_token = self.conf['notification']['line_notify_token']
        self.line_notify_api = self.conf['notification']['line_notify_api']
        self.headers = {'Authorization': 'Bearer ' + self.line_notify_token}
        self.payload = {'message': message}
        try:
            requests.post(self.line_notify_api, data=self.payload, headers=self.headers)
        except:
            error_time = dt.datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} NOTIFY_ERROR_001')