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

def get_years_month_debt_free(number_of_payments):
    date = get_datetime()
    year = int(date.year + number_of_payments / 12 ) - date.year
    month = number_of_payments % 12
    debt_free_on = ''
    if year > 0 and year < 1:
        debt_free_on = str(year) + ' year'
    if year > 1:
        month = month - 1
        debt_free_on = str(year) + ' years'
    if year > 0:
        debt_free_on = debt_free_on + ' '    
    if month == 1:
        debt_free_on = debt_free_on + str(month) +  ' month'
    if month > 1:
        debt_free_on = debt_free_on + str(month) + ' months'
    return debt_free_on    