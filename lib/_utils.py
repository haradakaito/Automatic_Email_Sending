import random
import jpholiday

from datetime import datetime

class Utils:
    def setting_wait_second(self) -> int:
        return int(abs(random.gauss(1200,2400)))
    
    def today_is_holiday(self) -> bool:
        return jpholiday.is_holiday(datetime.now()) or datetime.now().weekday() >= 5