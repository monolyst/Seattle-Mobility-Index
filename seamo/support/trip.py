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
    def __init__(self, origin, destination, mode, distance, duration, basket_category,
        pair, departure_time, rank, value_of_time_rate=cn.VOT_RATE):
        self.origin = self._convert_to_coord(origin)
        self.destination = self._convert_to_coord(destination)
        self.mode = mode
        self.distance = distance
        self.duration = self._calculate_duration(duration)
        self.basket_category = basket_category
        self.departure_time = departure_time
        self.pair = pair
        self.rank = rank
        self.value_of_time_rate = cn.VOT_RATE
        self.cost = self._calculate_base_cost(self.duration, self.value_of_time_rate)
        self.rank = rank
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.trip_id = None
        

    def _convert_to_coord(self, pair):
        pair = str(pair).split(", ")
        left = pair[0][1:]
        right = pair[1][:-1]
        return coordinate.Coordinate(left, right)

    def set_persona(self, persona):
        self.persona = persona

    def _calculate_base_cost(self, duration, value_of_time_rate=cn.VOT_RATE):
        return self.duration * value_of_time_rate / cn.MIN_TO_HR

    def _calculate_duration(self, duration):
        return duration

    def get_place(self, place, *args):
        if place == 'origin':
            place = self.origin
        elif place == 'destination':
            place = self.destination
        else:
            raise "not a place"
        print(place)
        for attribute in args:
            print(place.get_attribute(attribute))

    def get_trip_id(self, pair, mode, departure_time):
        #parse departure time
        self.departure_time = str(origin.block_group()) + '_' + pair + mode # + parsed departure time


class CarTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, pair, departure_time, rank,
        duration_in_traffic=0, mile_rate=cn.AAA_RATE):
        super().__init__(origin, destination, 'car', distance, duration, basket_category, pair, departure_time, rank)
        self.mile_rate = mile_rate
        self.cost_to_park = None
        self.parking_category = None
        self.duration_in_traffic = duration_in_traffic
        self.duration = self._calculate_car_duration(duration, duration_in_traffic)
        self.cost = self._calculate_cost(self.destination, self.duration, self.departure_time,
            self.mile_rate, self.value_of_time_rate)

    def _calculate_car_duration(self, duration, duration_in_traffic=0):
        # Not sure if this right
        return self.duration + self.duration_in_traffic

    def _calculate_cost(self, destination, duration, departure_time, mile_rate, value_of_time_rate):
        self.cost = super()._calculate_base_cost(self.duration)
        col = self._get_time_date(duration, departure_time)
        pc = parking_cost.ParkingCost()
        df = pc.geocode_point((float(destination.lat), float(destination.lon)))

        options = df.loc[:, (cn.PARKING_CATEGORY, str(col + cn.RATE))]
        options = options[options[cn.PARKING_CATEGORY] != cn.NO_PARKING_ALLOWED]
        options = options.loc[options[str(col + cn.RATE)].idxmin()].drop_duplicates()
        self.cost_to_park = int(options[str(col + cn.RATE)])
        self.parking_category = min(options[cn.PARKING_CATEGORY])
        return self.cost + (self.distance * self.mile_rate) + self.cost_to_park

    def _get_time_date(self, duration, departure_time):
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
    def __init__(self, origin, destination, distance, duration, basket_category, pair, departure_time, rank, fare_value,):
        super().__init__(origin, destination, 'transit', distance, duration, basket_category, pair, departure_time, rank)
        self.fare_value = fare_value
        self.cost = self._calculate_cost(self.fare_value)
        
    def _calculate_cost(self, fare_value):
        self.cost = super()._calculate_base_cost(self.duration)
        return self.cost + self.fare_value
    
class BikeTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, pair, departure_time, rank, bike_rate=cn.BIKE_RATE):
        super().__init__(origin, destination, 'bike', distance, duration, basket_category, pair, departure_time, rank)
        self.bike_rate = bike_rate
        self.cost = self._calculate_cost(self.distance, self.duration, self.bike_rate)

    def _calculate_cost(self, distance, duration, bike_rate):
        self.cost = super()._calculate_base_cost(self.duration)
        return self.cost + (self.distance * self.bike_rate)
    

class WalkTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, pair, departure_time, rank):
        super().__init__(origin, destination, 'walk', distance, duration, basket_category, pair, departure_time, rank)




