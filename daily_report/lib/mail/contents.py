import datetime as dt
import os
from ..progress.progress import Progress
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
        >>> contents = Contents(user_name='島田', user_grade='M1')
        >>> subject = contents.create_subject()
        >>> body = contents.create_body()

        Requirements(これらのファイルが必要):
        ---
        signature.txt
            署名を記述したテキストファイル
    """
    def __init__(self, user_name, user_grade):
        self.user_name = user_name  # メール作成者の名前
        self.user_grade = user_grade  # メール作成者の学年
        self.progress_getter = Progress()  # 進捗文を取得するクラス
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
        self.first  = '峰野研究室の皆様\n\n'
        self.first += f'峰野研究室{self.user_grade}の{self.user_name}です.\n'
        return self.first
    
    def _create_progress(self):
        """
            実施事項作成
        """
        progress_list = self.progress_getter.get_progress()
        progress = '本日の進捗を共有させていただきます.\n'
        progress += '本日は,'
        for prog in progress_list: progress += f'「{prog}」'
        progress += 'を行いました.\n'
        return progress
    
    def _create_progress_map(self):
        """
            進捗マップ作成
        """
        progress_map_list = self.progress_getter.get_progress_map()
        progress_map = '------◎本日実施，○実施中，●未実施，★完了------'
        for p in progress_map_list: progress_map += f'\n{p}'
        return progress_map
    
    def _create_plan(self):
        """
            今後の予定作成
        """
        plan_list = self.calendar.get_next_plan_list(self.user_name)
        plans = [f'{plan[0].replace("T", " ")[:-9]} : {plan[1]}\n' for plan in plan_list]
        plan = '-----今後の予定・その他-----\n'
        plan += ''.join(plans)
        return plan

    
    def _create_signature(self):
        """
            署名作成
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        signature_path = os.path.join(current_dir, 'signature.txt')
        with open(signature_path, 'r', encoding='UTF-8') as f:
            signature = f.read()

        return signature