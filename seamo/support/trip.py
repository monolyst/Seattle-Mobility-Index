import init
import constants as cn
from core import parking_cost, geocoder
from dateutil import parser

"""
Base Trip Class
"""
class Trip(object):
    def __init__(self, origin, destination, mode, distance, duration, category,
        pair, departure_time, rank):
        self.origin = origin
        self.destination = destination
        self.mode = mode
        self.distance = distance
        self.duration = self.__calculate_duration__(duration)
        self.category = category
        self.cost = self.__calculate_cost__(mode)
        self.rank = rank
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.trip_id = None
        self.parking_cost = None
        self.parking_category = None

    def set_persona(self, persona):
        self.persona = persona

    def __calculate_cost__(self):
        self.cost = 0

    def __calculate_duration__(self, duration):
        self.duration = duration

    def get_trip_id(self, pair, mode, departure_time):
        #parse departure time
        self.departure_time = str(origin.block_group()) + '_' + pair + mode # + parsed departure time


class CarTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category, mile_rate,
        value_of_time_rate=cn.AAA_RATE, duration_in_traffic=0):
        super().__init__(self, origin, destination, mode="car", distance, category)
        self.mile_rate = mile_rate
        self.value_of_time_rate = value_of_time_rate
        self.duration = self.__calculate_duration__(duration, duration_in_traffic)
        self.cost = self.__calculate_duration__(self.destination, self.duration,
            self.mile_rate, self.value_of_time_rate)

    def __calculate_cost__(self, destination, duration, mile_rate, value_of_time_rate):
        day_time = self.__get_time_date__(destination)
        pc = parking_cost.ParkingCost()
        df = pc.geocode_point((destination.lat, destination.lon))

        options = df.loc[:, (cn.PARKING_CATEGORY, str(col + cn.RATE))]
        options = options[options[cn.PARKING_CATEGORY] != cn.NO_PARKING_ALLOWED]
        options = options.loc[options[str(col + cn.RATE)].idxmin()].drop_duplicates()
        self.parking_cost = int(options[str(col + cn.RATE)])
        self.parking_category = min(options[cn.PARKING_CATEGORY])

        self.cost = distance * mile_rate + parking_cost + duration * value_of_time_rate / cn.MIN_TO_HR
        return cost

    def __get_time_date__(self, destination):
        date = parser.parse(date_time).date()
        time = parser.parse(date_time).time().replace(microsecond=0)
        
        if date.weekday() < 5:
            day_type = 'weekday'
        if time.hour >= 8 and time.hour <= 11:
            time_frame = 'morning'
        elif time.hour > 11 and time.hour <= 17:
            time_frame = 'afternoon'
        elif time.hour > 17 and time.hour <= 22:
            time_frame = 'evening'
        return day_type + '_' + time_frame + '_'



    def __calculate_duration__(self, duration, duration_in_traffic=0):
        # Not sure if this right
        self.duration = duration + duration_in_traffic



class TransitTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="transit", distance, category)

    def __calculate_cost__(self, fare_value):
        self.cost = fare_value
    


class BikeTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="bike", distance, category)

    

class WalkTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="walk", distance, category)
    

