import datetime as dt
import json
from pathlib import Path
from ..calendar import Calendar

class Contents:
    """
        Contents
        ===
        メール本文作成クラス

        Parameters:
        ---
        user_name : str
            メール作成者の名前
        user_grade : str
            メール作成者の学年

        Methods:
        ---
        create_subject()
            件名作成
        create_body()
            本文作成

        Usage:
        >>> contents = Contents(**user_info)
        >>> subject = contents.create_subject()
        >>> body = contents.create_body()
    """

    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../../config/config.json'

    def __init__(self, **user_info):
        self.user_info = user_info
        self.calendar = Calendar()  # カレンダーを取得するクラス

    def create_subject(self):
        """
            メール件名作成

            本日の進捗について(YYYY/MM/DD)
        """
        self.subject  = '本日の進捗について'
        self.subject += dt.datetime.now().strftime('(%Y/%m/%d)')
        return self.subject

    def create_body(self):
        """
            本文作成
        """
        # 最初の名乗り
        self.first = self._create_first()
        # 実施事項
        self.progress = self._create_progress()
        # 進捗マップ
        self.progress_map = self._create_progress_map()
        # 今後の予定
        self.plan = self._create_plan()
        # 署名
        self.signature = self._create_signature()
        # 本文作成
        self.body = self.first + self.progress + "\n\n" + self.progress_map + "\n\n" + self.plan + "\n\n" + self.signature
        return self.body
    
    def _create_first(self):
        """
            最初の言葉の作成
        """
        conf = json.load(open(self.conf_path, 'r', encoding='utf-8'))
        self.affiliation = conf['contents']['affiliation']
        self.first  = f'{self.affiliation}の皆様\n\n'
        self.first += f'{self.affiliation}{self.user_info["grade"]}の{self.user_info["name"]}です.\n'
        return self.first
    
    def _create_progress(self):
        """
            実施事項作成
        """
        progress = '本日の進捗を共有させていただきます.\n'
        progress += '本日は'
        progress += self.user_info['progress']
        progress += 'を行いました.'

        progress += self.user_info['other']

        return progress
    
    def _create_progress_map(self):
        """
            進捗マップ作成
        """
        progress_map  = '------◎本日実施，○実施中，●未実施，★完了------\n'
        progress_map += self.user_info['progress_map']
        return progress_map
    
    def _create_plan(self):
        """
            今後の予定作成
        """
        try:
            plan_list = self.calendar.get_next_plan_list(self.user_info['name'])
            plans = [f'{self._convert_plan_time(plan[0])}\t: {plan[1]}\n' for plan in plan_list]
            plan = '-----今後の予定・その他-----\n'
            plan += ''.join(plans)
            plan += '------------------------------\n'
        except:
            plan = ''

        return plan
    
    def _convert_plan_time(self, plan_time):
        """
            予定の時間を変換
        """
        if 'T' in plan_time:
            plan_time  = plan_time.replace('T', ' ')
            plan_time  = plan_time[:-9]
        else:
            plan_time += '\t'
        return plan_time

    def _create_signature(self):
        """
            署名作成
        """
        return self.user_info['signature']