import json
from datetime import datetime
from pathlib import Path

class Contents:

    """
        メールの件名や本文の作成クラス

        Parameters
        ----------
        None

        Attributes
        ----------
        AFFILIATION : str
            所属名
        
        Methods
        -------
        create_subject() -> str
            件名の作成
        
        create_first(user_info) -> str
            本文の冒頭部分の作成

        create_progress(user_info) -> str
            本文の進捗部分の作成

        create_progress_map(user_info) -> str
            本文の進捗マップ部分の作成
        
        create_event(user_event) -> str
            本文の予定部分の作成
        
        create_signature(user_info) -> str
            本文の署名部分の作成

        _convert_event_time(event_time) -> str
            予定の日時を整形する    
    """

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    conf        = json.load(open(conf_path, 'r', encoding='utf-8'))
    
    # クラス変数
    AFFILIATION = conf['contents']['AFFILIATION']

    def create_subject(self) -> str:
        """
            件名の作成

            Parameters
            ----------
            None

            Returns
            -------
            subject : str
                件名
        """
        subject  = '本日の進捗について'
        subject  += datetime.now().strftime('(%Y/%m/%d)')
        return subject

    def create_first(self, user_info:dict) -> str:
        """
            本文の冒頭部分の作成

            Parameters
            ----------
            user_info : dict
                ユーザ情報

            Returns
            -------
            first : str
                本文の冒頭部分
        """
        first  = f'{self.AFFILIATION}の皆様\n\n'
        first  += f'{self.AFFILIATION}{user_info["grade"]}の{user_info["name"]}です.\n\n'
        return first

    def create_progress(self, user_info:dict) -> str:
        """
            本文の進捗部分の作成

            Parameters
            ----------
            user_info : dict
                ユーザ情報

            Returns
            -------
            progress : str
                本文の進捗部分
        """
        progress = '本日の進捗を共有させていただきます.\n'
        progress += '本日は，' + user_info['progress'] + ' を行いました.'
        progress += user_info['other']
        return progress

    def create_progress_map(self, user_info:dict) -> str:
        """
            本文の進捗マップ部分の作成

            Parameters
            ----------
            user_info : dict
                ユーザ情報

            Returns
            -------
            progress_map : str
                本文の進捗マップ部分
        """
        progress_map  = '------◎本日実施，○実施中，●未実施，★完了------\n'
        progress_map  += user_info['progress_map']
        return progress_map

    def create_event(self, user_event:list) -> str:
        """
            本文の予定部分の作成

            Parameters
            ----------
            user_event : list
                ユーザ情報

            Returns
            -------
            event : str
                本文の予定部分
        """
        events = [f'{self._convert_event_time(tmp[0])}\t: {tmp[1]}\n' for tmp in user_event]
        event  = '-----今後の予定・その他-----\n'
        event  += ''.join(events)
        event  += '------------------------------\n'
        return event

    def _convert_event_time(self, event_time:str) -> str:
        if 'T' in event_time:
            event_time  = event_time.replace('T', ' ')
            event_time  = event_time[:-9]
        else:
            event_time  += '\t'
        return event_time

    def create_signature(self, user_info:dict) -> str:
        """
            本文の署名部分の作成

            Parameters
            ----------
            user_info : dict
                ユーザ情報

            Returns
            -------
            signature : str
                本文の署名部分
        """
        return user_info['signature']