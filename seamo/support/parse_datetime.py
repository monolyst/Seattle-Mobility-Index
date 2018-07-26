import init
from dateutil import parser
import datetime as dt
import constants as cn


class ParseDatetime(object):
    """
    This class parses a departure timestamp, and gives time interval, type of
    day, and parking time interval.
    """
    def __init__(self, departure_time, duration=0, parking=False):
        """
        Inputs: departure time, duration
        Outputs: time_interval and day_type
        If desired, user can choose to set parking_time_interval
        """
        self.departure_time = departure_time
        self.duration = duration
        self.time_interval = self._get_time(self.departure_time, self.duration)
        self.day_type = self._get_day(self.departure_time, self.duration)
        if parking:
            self.parking_time_interval = self._get_parking_time(self.departure_time, self.duration)


    def _get_time(self, departure_time, duration):
        """
        Inputs: departure_time, duration
        Outputs: time_interval
        """
        date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        time = date_time.time()
        return self._get_interval(time, cn.MORNING_START, cn.MORNING_END, cn.AFTERNOON_START,
            cn.AFTERNOON_END, cn.EVENING_START, cn.EVENING_END)


    def _get_day(self, departure_time):
        """
        Inputs: departure_time, duration
        Outputs: day_type
        """
        date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        date = date_time.date()
        if date.weekday() < cn.SATURDAY:
            day_type = cn.WEEKDAY
        else:
            day_type = cn.WEEKEND
        return day_type


    def _get_parking_time_interval(self, departure_time, duration=0):
        """
        Inputs: departure_time, duration
        Outputs: time_interval
        """
        date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        time = date_time.time()
        return self._get_interval(time, cn.PARKING_MORNING_START, cn.PARKING_MORNING_END,
            cn.PARKING_AFTERNOON_START, cn.PARKING_AFTERNOON_END, cn.PARKING_EVENING_START,
            cn.PARKING_EVENING_END)


    def _get_interval(self, time, morning_start, morning_end, afternoon_start, afternoon_end,
        evening_start, evening_end):
        """
        Helper method to get time interval.
        Inputs: time object, start and end times
        Outputs: time classification
        """
        if time.hour >= cn.MORNING_START and time.hour <= MORNING_END:
            time_frame = cn.MORNING
        elif time.hour > cn.AFTERNOON_START and time.hour <= cn.AFTERNOON_END:
            time_frame = cn.AFTERNOON
        elif time.hour > cn.EVENING_START and time.hour <= cn.EVENING_END:
            time_frame = cn.EVENING
        else:
            time_frame = cn.AFTER_HOURS
        return time_frame


        