from minelab.schedule import MineLabSchedule

def main():
    schedule = MineLabSchedule()
    print(f'本日のWR : {schedule.is_today_schedule(schedule_name="WR")}')
    print(f'本日のGMim : {schedule.is_today_schedule(schedule_name="GMim")}')
    print(f'本日のGMts : {schedule.is_today_schedule(schedule_name="GMts")}')

if __name__ == '__main__':
    main()