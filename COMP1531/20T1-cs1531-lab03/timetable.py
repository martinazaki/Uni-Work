from datetime import date, time, datetime

def timetable(dates, times):
    '''
    Generates a list of datetimes given a list of dates and a list of times. All possible combinations of date and time are contained within the result. The result is sorted in chronological order.

    For example,
    >>> timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)])
    [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]
    '''
    found = {}
    for date in dates:
        for time in times:
            found.append(datetime(date.year, date.month, date.day, time.hour, time.minute, time.second))
    found.sort()
    return found