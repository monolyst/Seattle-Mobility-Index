import init
import constants as cn
from core import parking_cost, geocoder
from support import coordinate
from dateutil import parser
import datetime as dt

"""
Base Trip Class
"""
class Trip(object):
    def __init__(self, origin, destination, mode, distance, duration, category,
        pair, departure_time, rank):
        print(origin)
        self.origin = self.__convert_to_coord__(origin)
        self.destination = self.__convert_to_coord__(destination)
        self.mode = mode
        self.distance = distance
        self.duration = self.__calculate_duration__(duration)
        self.category = category
        self.departure_time = departure_time
        self.pair = pair
        self.rank = rank
        self.cost = None #self.__calculate_cost__(mode)
        self.rank = rank
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.trip_id = None
        self.parking_cost = None
        self.parking_category = None

    def __convert_to_coord__(self, pair):
        pair = str(pair).split(", ")
        print(pair)
        left = pair[0][1:]
        right = pair[1][:-1]
        return coordinate.Coordinate(left, right)

    def set_persona(self, persona):
        self.persona = persona

    # def __calculate_cost__(self):
    #     self.cost = 0

    def __calculate_duration__(self, duration):
        self.duration = duration

    def get_place(self, place, **geocode_attributes):
        if place == self.origin or place == self.destination:
            print(place)
        else:
            raise "not a place"
        for attribute in geocode_attributes:
            print(place.attribute)

    def get_trip_id(self, pair, mode, departure_time):
        #parse departure time
        self.departure_time = str(origin.block_group()) + '_' + pair + mode # + parsed departure time


class CarTrip(Trip):
    def __init__(self, origin, destination, distance, duration, category, pair, departure_time, rank, 
                 mile_rate=cn.AAA_RATE, value_of_time_rate=cn.VOT_RATE, duration_in_traffic=0):
        super().__init__(origin, destination, 'car', distance, duration, category, pair, departure_time, rank)
        self.mile_rate = mile_rate
        self.cost_to_park = None
        self.parking_category = None
        self.value_of_time_rate = value_of_time_rate
        self.duration = self.__calculate_duration__(duration, duration_in_traffic)
        self.cost = self.__calculate_cost__(self.destination, self.duration, self.departure_time,
            self.mile_rate, self.value_of_time_rate)
        
    def __calculate_duration__(self, duration, duration_in_traffic=0):
        # Not sure if this right
        return self.duration + self.duration_in_traffic

    def __calculate_cost__(self, destination, duration, departure_time, mile_rate, value_of_time_rate):
#         super().__calculate_cost__()
        col = self.__get_time_date__(duration, departure_time)
        pc = parking_cost.ParkingCost()
        df = pc.geocode_point((float(destination.lat), float(destination.lon)))

        options = df.loc[:, (cn.PARKING_CATEGORY, str(col + cn.RATE))]
        options = options[options[cn.PARKING_CATEGORY] != cn.NO_PARKING_ALLOWED]
        options = options.loc[options[str(col + cn.RATE)].idxmin()].drop_duplicates()
        self.cost_to_park = int(options[str(col + cn.RATE)])
        self.parking_category = min(options[cn.PARKING_CATEGORY])
        return self.distance * self.mile_rate + self.cost_to_park + self.duration * self.value_of_time_rate / cn.MIN_TO_HR

    def __get_time_date__(self, duration, departure_time):
        date_time = parser.parse(departure_time) + dt.timedelta(minutes=float(duration))
        date = date_time.date()
        time = date_time.time()
        
        if date.weekday() < 5:
            day_type = 'weekday'
        if time.hour >= 8 and time.hour <= 11:
            time_frame = 'morning'
        elif time.hour > 11 and time.hour <= 17:
            time_frame = 'afternoon'
        elif time.hour > 17 and time.hour <= 22:
            time_frame = 'evening'
        return day_type + '_' + time_frame + '_'



class TransitTrip(Trip):
    def __init__(self, origin, destination, distance, category, pair, departure_time, rank):
        super().__init__(self, origin, destination, 'transit', distance, category, pair, departure_time, rank)

    def __calculate_cost__(self, fare_value):
        self.cost = fare_value
    


class BikeTrip(Trip):
    def __init__(self, origin, destination, distance, category, pair, departure_time, rank):
        super().__init__(self, origin, destination, 'bike', distance, category, pair, departure_time, rank)

    

class WalkTrip(Trip):
    def __init__(self, origin, destination, distance, category):
        super().__init__(self, origin, destination, 'walk', distance, category, pair, departure_time, rank)
