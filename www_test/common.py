import datetime
#from calendar import calendar

def get_number(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
        
def get_datetime():
    return datetime.datetime.now()        

def add_months(date, months):
    month = date.month - 1 + months
    year = int(date.year + month / 12 )
    month = month % 12 + 1
    #day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, date.day)
