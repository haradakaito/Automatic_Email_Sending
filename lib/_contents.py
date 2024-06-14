import json

from pathlib  import Path
from datetime import datetime

class Contents:

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / "../config/config.json"
    conf        = json.load(open(conf_path, "r", encoding="utf-8"))
    # クラス変数
    AFFILIATION = conf["contents"]["AFFILIATION"]

    def create_subject(self) -> str:
        return f"今週の進捗について({datetime.today().strftime("%Y/%m/%d")})"
    
    def create_body(self, name:str, grade:str, progress:str, progress_map:str, event:list, signature:str, free:str) -> str:
        body  = f"{self.AFFILIATION}の皆様\n\n"
        body += f"{self.AFFILIATION}{grade}の{name}です.\n\n"

        body += "本日の進捗を共有させていただきます.\n"
        body += f"本日は，{progress} を行いました."
        body += free
        body += "\n\n"

        body += "------◎本日実施，○実施中，●未実施，★完了------\n"
        body += progress_map
        body += "\n\n"

        body += "-----今後の予定・その他-----\n"
        body += "".join([f"{self._convert_event_time(tmp[0])}\t: {tmp[1]}\n" for tmp in event])
        body += "------------------------------\n"
        body += "\n\n"

        body += signature
        return body

    def _convert_event_time(self, event_time:str) -> str:
        if "T" in event_time:
            event_time = event_time.replace("T", " ")
            event_time = event_time[:-9]
        else:
            event_time += "\t"
        return event_time