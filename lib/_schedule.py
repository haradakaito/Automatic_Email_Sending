from datetime import datetime, timedelta, timezone

class Schedule:
    """
        スケジュールを管理するクラス

        Parameters
        ----------
        None

        Attributes
        ----------
        None

        Methods
        -------
        ical_parse(all_events, period:list) -> list
            icalファイルのパーサー
    """
    # icalファイルのパーサー
    def ical_parse(self, all_events, period:list):
        """
            icalファイルのパーサー

            Parameters
            ----------
            all_events : list
                icalファイルの情報
            period : list
                期間

            Returns
            -------
            event_list : list
                予定リスト
        """
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