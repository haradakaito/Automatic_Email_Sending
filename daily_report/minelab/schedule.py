from .calender import MineLabCalendarAPI

class MineLabSchedule:
    """
        MineLabSchedule
        ===
        峰野研究室のスケジュールをチェックするクラス

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
        >>> print(f'本質のGMts : {event.is_today_event(event_name="GMts")}')
    """
    def __init__(self):
        self.calendar = MineLabCalendarAPI()
    
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