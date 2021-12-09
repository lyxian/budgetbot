import calendar
import pendulum

WEEKDAYS = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun'
]

CATEGORIES = [
    "Food",
    "Shopping",
    "Transport",
    "Entertainment",
    "Miscellaneous"
]

OPERATORS = [
    "+",
    "-",
    "*",
    "/"
]

TEXT_PRICE = "{} @ {}\nEnter price: "
TEXT_DONE = "New record created at {}"

class CalendarObject():

    def __init__(self, now):
        self.year = now.year
        self.month = now.month
        self.monthName = calendar.month_name[now.month]
        self.days = calendar.monthcalendar(now.year, now.month)

def y(n=0):
    print(pendulum.now().add(months=n).month)

if __name__ == '__main__':
    pass