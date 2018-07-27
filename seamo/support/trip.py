import init
import pandas as pd
import constants as cn
from support import coordinate
from dateutil import parser
import datetime as dt
import support.seamo_exceptions as se
import numpy as np

"""
Base Trip Class
"""
class Trip(object):
    def __init__(self, origin, dest_lat, dest_lon, departure_time, mode, distance, duration, 
                basket_category, citywide_type=None, value_of_time_rate=cn.VOT_RATE):
        """
        Input:
            origin: string (a block group ID)
            dest_lat: float
            dest_lon: float
        """
        self.origin = origin
        self.destination = coordinate.Coordinate(dest_lat, dest_lon) 
        self.mode = mode
        self.departure_time = departure_time
        self.distance = distance
        self.duration = duration
        self.basket_category = basket_category
        self.citywide_type = citywide_type
        self.value_of_time_rate = cn.VOT_RATE
        self.cost = None
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.viable = None
        

    def set_cost(self):
        self.cost = self._calculate_base_cost(self.duration, self.value_of_time_rate)
        

    def set_viability(self, viability):
        """
        Input:
            viability (0 or 1)
        """
        self.viable = viability


    def get_origin_coordinate(self):
        """
        This returns a coordinate object. You can access centroid lat/lon and
        geocoded information from this object.
        """
        seattle_block_groups = pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP)
        df = seattle_block_groups[seattle_block_groups[cn.KEY] == self._origin]
        return coordinate.Coordinate(df.lat, df.lon)

    def set_persona(self, persona):
        self.persona = persona

    def _calculate_base_cost(self, duration, value_of_time_rate=cn.VOT_RATE):
        return duration * value_of_time_rate / cn.MIN_TO_HR

    def print_destination(self, *args):
        print(self._destination)
        for attribute in args:
            print(self._destination.get_attribute(attribute))


class CarTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, departure_time,
        duration_in_traffic=0, mile_rate=cn.AAA_RATE):
        super().__init__(origin, destination, 'car', distance, duration, basket_category, departure_time)
        self.destination = coordinate.Coordinate(dest_lat, dest_lon, geocode=True) 
        self.mile_rate = mile_rate
        self.cost_to_park = np.nan
        self.parking_category = None
        self.duration = self.duration_in_traffic
        self.cost = None

    def set_cost(self):
        self.cost = self._calculate_cost(self.destination, self.duration, self.departure_time,
            self.mile_rate, self.value_of_time_rate)

    def _calculate_car_duration(self, duration, duration_in_traffic=0):
        #TODO: do I want to save the original duration for car trips?
        return duration_in_traffic

    def _calculate_cost(self, destination, duration, departure_time, mile_rate, value_of_time_rate):
        self.cost = super()._calculate_base_cost(self.duration)
        parking_cost = pd.read_csv(cn.BLOCK_GROUP_PARKING_RATES_FP)
        self.cost_to_park = parking_cost.loc(destination.block_group, cn.RATE)
        return self.cost + (self.distance * mile_rate) + self.cost_to_park


class TransitTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, departure_time, fare_value):
        super().__init__(origin, destination, 'car', distance, duration, basket_category, departure_time)
        self.fare_value = fare_value
        self.cost = None

    def set_cost(self):
        self.cost = self._calculate_cost(self.fare_value)
        
    def _calculate_cost(self, fare_value):
        self.cost = super()._calculate_base_cost(self.duration)
        return self.cost + fare_value
    
class BikeTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, departure_time, bike_rate=cn.BIKE_RATE):
        super().__init__(origin, destination, 'car', distance, duration, basket_category, departure_time)
        self.bike_rate = bike_rate
        self.cost = None

    def set_cost(self):
        self.cost = self._calculate_cost(self.distance, self.duration, self.bike_rate)

    def _calculate_cost(self, distance, duration, bike_rate):
        self.cost = super()._calculate_base_cost(self.duration)
        return self.cost + (distance * bike_rate)
    

class WalkTrip(Trip):
    def __init__(self, origin, destination, distance, duration, basket_category, departure_time):
        super().__init__(origin, destination, 'car', distance, duration, basket_category, departure_time)




