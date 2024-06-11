import json
import random
import requests
import jpholiday
from datetime import datetime
from icalendar import Calendar
from notion_client import Client
from pathlib import Path

from _database import Database
from _schedule import Schedule
from _contents import Contents

class Getutils:
    """
        データベースの情報を取得するクラス

        Parameters
        ----------
        None

        Attributes
        ----------
        NOTION_ACCESS_TOKEN : str
            Notionのアクセストークン

        NOTION_MASTER_ID : str
            マスターデータベースのID

        ICAL_URL : str
            iCalendarのURL
        
        Methods
        -------
        today_is_holiday() -> bool
            休日かどうかを取得する

        get_sleep_time(num) -> list
            ランダムな送信時刻を取得

        get_all_db_info() -> list
            全ユーザーのデータベース情報を取得

        _get_all_dbid() -> list
            全ユーザーのデータベースIDを取得

        _get_db_info(dbid:str) -> dict
            データベースIDに対応するDBの情報を取得

        get_all_user_event(all_db_info:list) -> list
            全ユーザーの予定を取得

        _get_user_event(user_name:str) -> list
            ユーザーの1週間分の予定を取得

        all_get_user_subject(all_db_info:list) -> list
            全ユーザーの件名を取得

        _get_subject() -> str
            件名の取得

        get_all_user_body(all_user_info:list, all_user_event:list) -> list
            全ユーザーの本文を取得

        _get_body(user_info:dict, user_event:list) -> str
            本文の取得
    """

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    conf        = json.load(open(conf_path, 'r', encoding='utf-8'))

    # クラス変数
    NOTION_ACCESS_TOKEN = conf['master']['NOTION_ACCESS_TOKEN']
    NOTION_MASTER_ID    = conf['master']['NOTION_MASTER_ID']
    ICAL_URL            = conf['calendar']['ICAL_URL']

    def __init__(self):
        self.client     = Client(auth=self.NOTION_ACCESS_TOKEN)
        self.database   = Database()
        self.schedule   = Schedule()
        self.contents   = Contents()

    # 休日かどうかを取得する
    def today_is_holiday(self) -> bool:
        """
            休日かどうかを取得する

            Parameters
            ----------
            None

            Returns
            -------
            bool
                休日かどうか

            Notes
            -----
            本日が休日かどうかを取得する
        """
        try:
            date = datetime.now()
            return jpholiday.is_holiday(date) or date.weekday() >= 5
        except:
            return None
    
    # 全ユーザーのデータベース情報を取得
    def get_all_db_info(self) -> list:
        """
            全ユーザーのデータベース情報を取得

            Parameters
            ----------
            None

            Returns
            -------
            list
                全ユーザーのデータベース情報

            Notes
            -----
            全ユーザーのデータベースIDを取得し，そのIDに対応するデータベース情報を取得する
        """
        all_dbid = self._get_all_dbid()
        all_db_info = [self._get_db_info(dbid) for dbid in all_dbid if self._get_db_info(dbid) != None]
        return all_db_info

    # 全ユーザーのデータベースIDを取得
    def _get_all_dbid(self) -> list:
        r = self.client.databases.query(self.NOTION_MASTER_ID)
        all_dbid_list = []
        try:
            for i in range(len(r['results'])):
                id = r['results'][i]['properties']['データベースID']['title'][0]['plain_text']
                all_dbid_list.append(id)
            return all_dbid_list
        except:
            return None

    # データベースIDに対応するDBの情報を取得
    def _get_db_info(self, dbid:str) -> dict:
        r = self.client.databases.query(dbid)
        try:
            db_info_dict = self.database.db_info_parse(r)
            return db_info_dict
        except:
            return None
    
    # 全ユーザーの件名を取得
    def get_all_user_subject(self, all_db_info:list) -> list:
        """
            全ユーザーの件名を取得

            Parameters
            ----------
            all_db_info : list
                全ユーザーのデータベース情報

            Returns
            -------
            list
                全ユーザーの件名
        """
        all_user_subject = [self._get_subject() for db_info in all_db_info if db_info['flag'] == True]
        return all_user_subject
    
    # 件名の取得
    def _get_subject(self) -> str:
        try:
            subject  = '本日の進捗について'
            subject  += datetime.now().strftime('(%Y/%m/%d)')
            return subject
        except:
            return None
    
    # 全ユーザーの本文を取得
    def get_all_user_body(self, all_db_info:list) -> list:
        """
            全ユーザーの本文を取得

            Parameters
            ----------
            all_db_info : list
                全ユーザーのデータベース情報

            Returns
            -------
            list
                全ユーザーの本文
        """
        all_user_event = [self._get_user_event(db_info['name']) for db_info in all_db_info if db_info['flag'] == True]
        all_user_body  = [self._get_body(user_info, user_event) for user_info, user_event in zip(all_db_info, all_user_event)]
        return all_user_body
    
    # 本文の取得
    def _get_body(self, user_info:dict, user_event:list) -> str:
        try:
            first           = self.contents.create_first(user_info)
            progress        = self.contents.create_progress(user_info)
            progress_map    = self.contents.create_progress_map(user_info)
            event           = self.contents.create_event(user_event)
            signature       = self.contents.create_signature(user_info)
            body = first + progress + "\n\n" + progress_map + "\n\n" + event + "\n\n" + signature
            return body
        except:
            return None

    # ユーザーの1週間分の予定を取得
    def _get_user_event(self, user_name:str) -> list:
        ical = requests.get(self.ICAL_URL)
        ical.raise_for_status()
        ical = Calendar.from_ical(ical.text)
        all_events      = [tmp for tmp in ical.walk('VEVENT')]
        all_user_events = [tmp for tmp in all_events if user_name in tmp.get('SUMMARY')]
        try:
            user_event = self.schedule.ical_parse(all_user_events, period=[1, 8])
            return user_event
        except:
            return None
    
    # ランダムな送信時刻を取得
    def get_all_sleeptime(self, all_db_info:list) -> list:
        """
            全ユーザーの送信時刻を取得

            Parameters
            ----------
            all_db_info : list
                全ユーザーのデータベース情報

            Returns
            -------
            list
                全ユーザーの送信時刻
        """
        all_sleeptime = []
        for db_info in all_db_info:
            if db_info['flag'] == True:
                all_sleeptime.append([db_info['name'], db_info['flag'], (int(abs(random.gauss(1200,2400)))) ])
            else:
                all_sleeptime.append([db_info['name'], db_info['flag'], -1                                  ])
        return all_sleeptime
    
    # メール送信ユーティリティを取得
    def get_pass_email(self, all_db_info:list) -> list:
        """
            メール送信ユーティリティを取得

            Parameters
            ----------
            all_db_info : list
                全ユーザーのデータベース情報

            Returns
            -------
            list
                メール送信ユーティリティ
        """
        all_password    = [db_info['password'] for db_info in all_db_info if db_info['flag'] == True]
        all_email       = [db_info['email']    for db_info in all_db_info if db_info['flag'] == True]
        return all_password, all_email

    # プロパティを更新
    def _update_property(self, db_id:str, property_name:str, new_contents:str) -> None:
        """
            指定したプロパティを更新

            Parameters
            ----------
            db_id : str
                データベースID
            
            property_name : str
                プロパティ名

            new_contents : str
                更新する内容

            Returns
            -------
            None
        """

        r = self.client.databases.query(db_id)
        self.client.pages.update(page_id=r['results'][0]['id'],
                                    properties={
                                        property_name: {
                                            'rich_text': [
                                                {
                                                    'type':'text', 'text':{
                                                        'content':{new_contents}
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    )