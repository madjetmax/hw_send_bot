from calendar import monthrange
from typing import Tuple
import datetime

def gen_week_days():
    day = datetime.datetime.now().strftime("%A").lower()[:3]
    mon = None
    tue = None
    wed = None
    thu = None
    fri = None

    n_mon = None
    n_tue = None
    n_wed = None
    n_thu = None
    n_fri = None



    if day == 'mon':
        mon = datetime.datetime.today()
        tue = datetime.datetime.today() + datetime.timedelta(1)
        wed = datetime.datetime.today() + datetime.timedelta(2)
        thu = datetime.datetime.today() + datetime.timedelta(3)
        fri = datetime.datetime.today() + datetime.timedelta(4)

        days_offset = 6

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)


    if day == 'tue':
        tue = datetime.datetime.today()

        wed = datetime.datetime.today() + datetime.timedelta(1)
        thu = datetime.datetime.today() + datetime.timedelta(2)
        fri = datetime.datetime.today() + datetime.timedelta(3)

        days_offset = 5

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)
    
    if day == 'wed':
        wed = datetime.datetime.today()

        thu = datetime.datetime.today() + datetime.timedelta(1)
        fri = datetime.datetime.today() + datetime.timedelta(2)

        days_offset = 4

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)
    
    if day == "thu":
        thu = datetime.datetime.today()

        fri = datetime.datetime.today() + datetime.timedelta(1)
        days_offset = 3

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)

    if day == "fri":
        fri = datetime.datetime.today()
        days_offset = 2

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)
    
    if day == "sat":
        days_offset = 1

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)

    if day == "sun":
        days_offset = 0

        n_mon = datetime.datetime.today() + datetime.timedelta(1+days_offset)
        n_tue = datetime.datetime.today() + datetime.timedelta(2+days_offset)
        n_wed = datetime.datetime.today() + datetime.timedelta(3+days_offset)
        n_thu = datetime.datetime.today() + datetime.timedelta(4+days_offset)
        n_fri = datetime.datetime.today() + datetime.timedelta(5+days_offset)

    return (
        [
            ["mon", mon], 
            ["tue", tue], 
            ["wed", wed], 
            ["thu", thu], 
            ["fri", fri]
        ],
        [
            ["mon", n_mon], 
            ["tue", n_tue], 
            ["wed", n_wed], 
            ["thu", n_thu], 
            ["fri", n_fri]
        ])

def get_next_day() -> str:
    date = datetime.datetime.today() + datetime.timedelta(1)

    return (str(date.date()), date.strftime("%A"))