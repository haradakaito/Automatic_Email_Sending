from .calendar import Calendar
import jpholiday
import datetime as dt

class Schedule:
    """
        Schedule
        ===
        スケジュールをチェックするクラス

        Parameters
        ---
        None
        
        Methods
        ---
        is_today_schedule()
            本日のイベントを取得
            
        Usage
        ---
        ```python
        >>> event = MineLabEvent()
        >>> print(f'本日のWR : {event.is_today_event(event_name="WR")}')
        >>> print(f'本日のGMim : {event.is_today_event(event_name="GMim")}')
        >>> print(f'本日のGMts : {event.is_today_event(event_name="GMts")}')
    """
    def __init__(self):
        self.calendar = Calendar()

    def is_today_holiday(self) -> bool:
        """
            本日が休日かどうかを判定

            Parameters
            ---
            None

            Returns
            ---
            bool
                本日が休日の場合はTrue、平日の場合はFalse
        """
        # 祝日かどうか
        is_holiday = jpholiday.is_holiday(dt.date.today())
        # 土日かどうか
        is_weekend = (dt.datetime.now().weekday() == 5) or (dt.datetime.now().weekday() == 6)
        return is_holiday or is_weekend

    
    def is_today_schedule(self, schedule_name:str) -> bool:
        """
            本日特定のイベントがあるかどうかを判定

            Parameters
            ---
            schedule_name : str
                スケジュール名

            Returns
            ---
            bool
                [スケジュール名]がある場合はTrue、ない場合はFalse
        """
        today_schedule = self.calendar.get_today_events()
        for event in today_schedule:
            if schedule_name in event[1]:
                return True
        return False