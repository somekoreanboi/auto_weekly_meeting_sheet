from datetime import datetime  # 1
from datetime import timedelta  # 2


class TimeService:

    def week_no(self, y, m, d):
        """ 연월일을 입력받아 해당 요일의 주차를 얻는 함수

        Args:
            y (int) - 연도
            m (int) - 월
            d (int) - 일

        Return:
            int - 해당 요일의 주
        """

        def _ymd_to_datetime(y, m, d):  # 3
            """ 연월일을 입력받아 datetime 객체로 변환하는 함수

            Args:
                y (int) - 연도
                m (int) - 월
                d (int) - 일

            Return:
                datetime - YYYY-MM-DD 형식의 datetime 객체
            """

            s = f'{y:04d}-{m:02d}-{d:02d}'
            return datetime.strptime(s, '%Y-%m-%d')

        target_day = _ymd_to_datetime(y, m, d)  # 4
        firstday = target_day.replace(day=1)  # 5
        while firstday.weekday() != 0:  # 6
            firstday += timedelta(days=1)

        if target_day < firstday:  # 7
            return 1

        return (target_day - firstday).days // 7 + 2  # 8

    # 목요일 실행이므로 1일을 더하면 금요일이 나옴; 금요일이 포함된게 기준임
    def get_this_friday(self):
        this_friday = datetime.today() + timedelta(days=3)
        year = int(this_friday.year)
        month = int(this_friday.month)
        day = int(this_friday.day)
        nth_week = self.week_no(year, month, day)

        return [year, month, nth_week]

    # 목요일 실행이므로 8일을 더하면 금요일이 나옴; 금요일이 포함된게 기준임
    def get_next_friday(self):
        this_friday = datetime.today() + timedelta(days=8)
        year = int(this_friday.year)
        month = int(this_friday.month)
        day = int(this_friday.day)
        nth_week = self.week_no(year, month, day)

        return [year, month, nth_week]

    def get_next_week(self):
        next_monday = datetime.today() + timedelta(days=4)
        next_friday = datetime.today() + timedelta(days=8)

        return next_monday.strftime("%Y.%m.%d") + '~' + next_friday.strftime("%Y.%m.%d")



