import json
import requests
from icalendar import Calendar as cl
from datetime import datetime, timedelta, timezone
from pathlib import Path

class Calendar:
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / "../config/config.json"
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    def __init__(self):
        """
        icalデータを取得する

        Parameters
        ---
        None
        """
        self.ical_url = self.conf['calendar']['ical_url']
        self.ical = self._download_data(self.ical_url)
        self.ical = self._parse_ical(self.ical)
    
    def _download_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    def _parse_ical(self, ical):
        return cl.from_ical(ical)
    
    def get_next_plan_list(self, user_name) -> list:
        """
        ユーザーの予定を取得する

        Parameters
        ---
        user_name : str
            ユーザー名
        """
        events = [event for event in self.ical.walk('VEVENT')]
        events = [event for event in events if user_name in event.get('SUMMARY')]
        start_dt = datetime.now().replace(tzinfo=timezone.utc).date() + timedelta(days=1)
        end_dt = start_dt + timedelta(days=7)
        events = [event for event in events if start_dt <= self._datetime_to_date(event.get('DTSTART').dt) <= end_dt]
        events = sorted(events, key=lambda x: self._datetime_to_date(x.get('DTSTART').dt))
        event_list = []
        for event in events:
            dtstart = self._change_timezone(event.get('DTSTART').dt)
            dtstart = dtstart.strftime('%Y/%m/%d %H:%M')
            summary = str(event.get('SUMMARY'))
            event_list.append((dtstart, summary))
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

# if __name__ == "__main__":
#     cal = Calendar()
#     cal.get_next_plan_list("島田")