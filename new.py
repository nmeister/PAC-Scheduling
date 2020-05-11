from datetime import date, timedelta

sdate = date(2008, 8, 15)   # start date
edate = date(2008, 9, 15)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    print(day)
