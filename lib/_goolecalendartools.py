import json
import requests

from pathlib   import Path
from datetime  import datetime, timedelta, timezone
from icalendar import Calendar

class GoogleCalendarTools:

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    conf        = json.load(open(conf_path, 'r', encoding='utf-8'))
    # クラス変数
    ICAL_URL = conf['calendar']['ICAL_URL']

    # ユーザーの1週間分の予定を取得
    def get_event(self, username:str) -> list:
        ical = requests.get(self.ICAL_URL)
        ical.raise_for_status()
        ical = Calendar.from_ical(ical.text)
        all_events      = [tmp for tmp in ical.walk('VEVENT')]
        all_user_events = [tmp for tmp in all_events if username in tmp.get('SUMMARY')]
        user_event = self._ical_parse(all_user_events, period=[1, 8])
        return user_event

    def _ical_parse(self, all_events, period:list):
        start_dt = datetime.now().replace(tzinfo=timezone.utc).date() + timedelta(days=period[0])
        end_dt   = datetime.now().replace(tzinfo=timezone.utc).date() + timedelta(days=period[1])
        events   = [tmp for tmp in all_events if start_dt <= self._datetime_to_date(tmp.get('DTSTART').dt) <= end_dt]
        events   = sorted(events, key=lambda x: self._datetime_to_date(x.get('DTSTART').dt))
        event_list = []
        for e in events:
            event_time = self._change_timezone(e.get('DTSTART').dt).strftime('%Y/%m/%d %H:%M')
            event_name = str(e.get('SUMMARY'))
            event_list.append((event_time, event_name))
        return event_list
    
    def _change_timezone(self, src):
        if isinstance(src, datetime):
            return src.astimezone(timezone(timedelta(hours=9)))
        else:
            return src
    
    def _datetime_to_date(self, src):
        if isinstance(src, datetime):
            return src.date()
        else:
            return src