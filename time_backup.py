import datetime


class TimeService:

    def __init__(self):
        self.today = datetime.datetime.today()
        self.monday = self.today - datetime.timedelta(days=3)

    def get_current(self):
        return datetime.datetime.now()

    def get_next_year(self):
        return self.monday.year

    def get_next_month(self):
        return self.monday.month

    def get_next_week(self, before_week):
        next_date = self.monday + datetime.timedelta(days=7)
        if self.monday.month == next_date.month:
            return before_week + 1
        else:
            return 1

    def get_this_week_range(self):
        monday = self.monday.strftime("%Y.%m.%d")
        friday = self.today + datetime.timedelta(days=1)
        friday = friday.strftime("%Y.%m.%d")
        result = monday + '~' + friday

        return result

# print(TimeService().get_this_week_range())
