import init
from dateutil import parser
import datetime as dt
import constants as cn

date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        date = date_time.date()
        time = date_time.time()
        
        if date.weekday() < 5:
            day_type = 'weekday'
        else:
            day_type = 'weekend'
        if time.hour >= 8 and time.hour <= 11:
            time_frame = 'morning'
        elif time.hour > 11 and time.hour <= 17:
            time_frame = 'afternoon'
        elif time.hour > 17 and time.hour <= 22:
            time_frame = 'evening'
        else:
            time_frame = None #fix default value