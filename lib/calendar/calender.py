from datetime import datetime
from icalendar import Calendar as cl
from datetime import datetime, timedelta, timezone

import json
from pathlib import Path
import requests

class Calendar:
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / "../../config/config.json"
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    def __init__(self):
        self.ical_url = self.conf['calendar']['ical_url']
        self.ical = self.__download_data(self.ical_url)
        self.ical = self.__parse_ical(self.ical)
    
    def __download_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    def __parse_ical(self, ical):
        return cl.from_ical(ical)
    
    def get_next_plan_list(self, user_name):
        # user_nameがSUMMARYに含まれているイベントを取得
        events = [event for event in self.ical.walk('VEVENT')]
        events = [event for event in events if user_name in event.get('SUMMARY')]
        start_dt = datetime.now().replace(tzinfo=timezone.utc).date() + timedelta(days=1)
        end_dt = start_dt + timedelta(days=7)
        events = [event for event in events if start_dt <= self.__datetime_to_date(event.get('DTSTART').dt) <= end_dt]
        events = sorted(events, key=lambda x: x.get('DTSTART').dt)
        event_list = []
        for event in events:
            dtstart = self.__change_timezone(event.get('DTSTART').dt)
            dtstart = dtstart.strftime('%Y/%m/%d %H:%M')
            summary = str(event.get('SUMMARY'))
            event_list.append((dtstart, summary))
        return event_list
    
    def __change_timezone(self, src):
        if isinstance(src, datetime):
            return src.astimezone(timezone(timedelta(hours=9)))
        else:
            return src
    
    def __datetime_to_date(self, src):
        if isinstance(src, datetime):
            return src.date()
        else:
            return src

if __name__ == "__main__":
    cal = Calendar()
    cal.get_next_plan_list("島田")