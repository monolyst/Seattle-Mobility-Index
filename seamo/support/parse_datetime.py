import init
from dateutil import parser
import datetime as dt
import constants as cn


class ParseDatetime(object):
    """
    This class parses a departure timestamp 9string), and gives time interval (MORNING, AFTERNOON 
    or EVENING), type of day (WEEKDAY or WEEKEND), and parking time interval (blocks of time with distinct
    parking rates). For details of the threasholds for all time intervals, refer to the constants file.
    """
    def __init__(self, departure_time, duration=0, parking=False):
        """
        Inputs: departure time (string), duration (float), parking (boolean, default=True)
        Outputs: time_interval (string) and day_type (string)
        If desired, user can choose to set a parking_time_interval (string)
        """
        self.departure_time = departure_time
        self.duration = duration
        self.time_interval = self._get_time(self.departure_time, self.duration)
        self.day_type = self._get_day(self.departure_time, self.duration)
        if parking:
            self.parking_time_interval = self._get_parking_time(self.departure_time, self.duration)


    def _get_time(self, departure_time, duration):
        """
        This function classifies a given time within SDOTs time categories (MORNING, AFTERNOON, EVENING)
        Inputs: departure_time (string), duration (float)
        Outputs: time_interval (string)
        """
        date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        time = date_time.time()
        return self._get_interval(time, cn.MORNING_START, cn.MORNING_END, cn.AFTERNOON_START,
            cn.AFTERNOON_END, cn.EVENING_START, cn.EVENING_END)


    def _get_day(self, departure_time):
        """
        Takes in a date_time + trip duration and classifies as WEEKDAY or WEEKEND
        Inputs: departure_time (string), duration (duration)
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
        Takes in a date_time + trip duration and classifies within SDOT's parking
        time intervals (for parking fee rates)
        Inputs: departure_time (string), duration (float)
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
        Helper method to get a time interval given specific thresholds.
        Inputs: time object, start and end times
        Outputs: time classification
        """
        if time.hour >= morning_start and time.hour <= morning_end:
            time_frame = cn.MORNING
        elif time.hour > afternoon_start and time.hour <= afternoon_end:
            time_frame = cn.AFTERNOON
        elif time.hour > evening_start and time.hour <= evening_end:
            time_frame = cn.EVENING
        else:
            time_frame = cn.AFTER_HOURS
        return time_frame


        