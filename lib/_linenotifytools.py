import json
import requests

from pathlib  import Path
from datetime import datetime, timedelta

class Linenotifytools:

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / "../config/config.json"
    conf        = json.load(open(conf_path, "r", encoding="utf-8"))
    # クラス変数
    LINE_NOTIFY_TOKEN       = conf["notification"]["LINE_NOTIFY_TOKEN"]
    TEST_LINE_NOTIFY_TOKEN  = conf["notification"]["TEST_LINE_NOTIFY_TOKEN"] # テスト用
    LINE_NOTIFY_API         = conf["notification"]["LINE_NOTIFY_API"]

    def notify_check_result(self, check_result:list, correctable_time:datetime) -> None:
        msg  = f"{datetime.today().strftime("%Y/%m/%d")}\n\n"
        msg  += f"送信可否（{correctable_time.strftime("%H:%M")}まで修正可能）\n"
        msg  += "-----------------------------\n"
        for username, flag, _ in check_result:
            if flag:
                msg += f"{username}: ○\n"
            else:
                msg += f"{username}: ✖\n"
        msg  += "-----------------------------"
        self._send_notify(msg)
    
    def notify_sendtime(self, all_username:list, all_wait_second:list) -> None:
        msg  = f"{datetime.today().strftime("%Y/%m/%d")}\n\n"
        msg  += "送信予定時刻\n"
        msg  += "-----------------------------\n"
        for username, wait_second in zip(all_username, all_wait_second):
            sendtime = datetime.now() + timedelta(seconds=wait_second)
            msg += f"{username}: {sendtime.strftime("%H:%M")}\n"
        msg  += "-----------------------------"
        self._send_notify(msg)

    def _send_notify(self, msg:str) -> None:
        payload = {"message": msg}
        headers = {"Authorization": "Bearer " + self.LINE_NOTIFY_TOKEN}
        # headers = {"Authorization": "Bearer " + self.TEST_LINE_NOTIFY_TOKEN} # テスト用
        requests.post(self.LINE_NOTIFY_API, data=payload, headers=headers)