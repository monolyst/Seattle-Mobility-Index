import init
import pandas as pd
import constants as cn
from support import coordinate
from dateutil import parser
import datetime as dt
import support.seamo_exceptions as se
import numpy as np

"""
Trip base class.

    A trip is one of the base inputs for the Mobility Index. This class is created to facilitate
    the use of trips as units of analysis within the individual Index Calculators (Mode choice, affordability, reliability).
    The Trip Object is used to represent an individual Trip and store and keep track of its core attributes and 
    defining variables.

    Attributes:
        origin: Block Group ID (string) of place where the trip originated.
        destination: Coordinates of destination latitude and longitude (dest_lat, dest_lon)
        mode: mode of the trip (WALKING,TRANSIT, DRIVING, CYCLING)
        departure_time: string indicating the time when the trip started
        distance: float indicating distance travelled between origin and destination.
        duration: float indicating the time elapsed between origin and destination.
        basket_category: string indicating the type of destination (i.e. school, hospital, pharmacy, post office, citywide destination, urban village, etc.)
        citywide_type: string that stores categories for citywide destinations
        value_of_time_rate: float, rate used as base for cost, representing opportunity cost of travel time
        cost = float indicating the full cost of the trip
        viable: value between 0 and 1 indicating the level of viability of the trip, as determined by the mode choice calculator.

    TODO:
    Revise attributes
            persona = None * is a persona an attribute of a trip? Need to define
            time_of_day (do we need this?)
            type_of_day = None (do we need this?)
 
"""
class Trip(object):
    def __init__(self, mode, origin, dest_lat, dest_lon, distance, duration, 
                basket_category, departure_time, citywide_type=None, value_of_time_rate=cn.VOT_RATE, place_name=None):
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
        self.place_name = place_name
        self.cost = None
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.viable = None
        self.dest_blockgroup = None
        self.neighborhood_long = None
        self.neighborhood_short = None
        self.council_district = None
        self.urban_village = None
        self.zipcode = None

    def set_geocoded_attributes(self, dest_blockgroup, neighborhood_long, neighborhood_short,
                                council_district, urban_village, zipcode):
        self.dest_blockgroup = dest_blockgroup
        self.neighborhood_long = neighborhood_long
        self.neighborhood_short = neighborhood_short
        self.council_district = council_district
        self.urban_village = urban_village
        self.zipcode = zipcode
        self.destination.set_geocoded_attributes(dest_blockgroup, neighborhood_long,
            neighborhood_short, council_district, urban_village, zipcode)
        return self
        

    def set_cost(self):
        """
        Sets the cost of the trip based on the base rate. 
        Only includes cost value of time.
        """
        self.cost = self._calculate_base_cost(self.duration, self.value_of_time_rate)
        return self
        

    def set_viability(self, viability):
        """
        Sets the viability of the trip. 
        The value of viability can be determined using the mode choice calculator.
        Input:
            viability (float between 0 and 1)
        """
        self.viable = viability


    def get_origin_coordinate(self):
        """
        This function returns a coordinate object that allows you to access the centroid lat/lon
        of the  origin blockgroup and store the geocoded information of this object.
        """
        seattle_block_groups = pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP)
        df = seattle_block_groups[seattle_block_groups[cn.KEY] == self._origin]
        return coordinate.Coordinate(df.lat, df.lon)

    
    def set_persona(self, persona):
        """
        TODO: define how personas will relate to trip object. Currently unclear.
        """
        self.persona = persona

    def _calculate_base_cost(self, duration, value_of_time_rate=cn.VOT_RATE):
        """
        Estimates trip cost from base rate. Includes only costs from time spent on trip.
        """
        return duration * value_of_time_rate / cn.MIN_TO_HR

    def print_destination(self, *args):
        """
        Prints the geocoded 
        Arguments are optional and can include any or all of the geocode attributes of a destination
        such as blockgroup, neighborhood, zip code, council district, urban village, etc.

        TODO: Make sure all the correct possible args are listed.
        """
        print(self._destination)
        for attribute in args:
            print(self._destination.get_attribute(attribute))


class CarTrip(Trip):
    """
    Child class of Trip for trips made by car.
    The distingusihing features are that car trips duration is based on time spent in traffic
    and cost methods are specific to those incurred when driving (for example gas and parking).

    TODO: refactor self.destination in child constructor.
    """
    def __init__(self, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time,
        duration_in_traffic=0, mile_rate=cn.AAA_RATE):
        super().__init__(cn.DRIVING_MODE, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time)
        self.mile_rate = mile_rate
        self.cost_to_park = None
        self.parking_category = None
        self.duration = duration_in_traffic
        self.cost = None

    def set_cost(self):
        """
        sets cost of a car trip.
        """
        self.cost = self._calculate_cost(self.destination, self.duration, self.departure_time,
            self.mile_rate, self.value_of_time_rate)
        return self
      

    def _calculate_car_duration(self, duration, duration_in_traffic=0):
        #TODO: do I want to save the original duration for car trips?
        #TODO: make a specific exception for no min
        return duration_in_traffic + cn.PARKING_TIME_OFFSET

    def _calculate_cost(self, destination, duration, departure_time, mile_rate, value_of_time_rate):
        """
        Cost methods to estimate costs during car trip (for example gas and parking)
        """
        self.cost = super()._calculate_base_cost(duration)
        destination.set_parking_cost()
        self.cost_to_park = destination.parking_cost
        # try:
        #     destination.set_geocode()
        #     # parking_cost = pd.read_csv(cn.BLOCK_GROUP_PARKING_RATES_FP)
        #     # self.cost_to_park = min(parking_cost.loc[parking_cost[cn.KEY] == destination.block_group, cn.RATE])
        # except: #(se.NotInSeattleError, ValueError) as e:
        #     pass
        
        # else
        # parking_cost = pd.read_csv(cn.BLOCK_GROUP_PARKING_RATES_FP)
        # try:
        #     min(parking_cost.loc[parking_cost[cn.KEY] == destination.block_group, cn.RATE])
        # except ValueError:
        #     self.cost_to_park = 0
        # else:
        #     self.cost_to_park = min(parking_cost.loc[parking_cost[cn.KEY] == destination.block_group, cn.RATE])
        return self.cost + (self.distance * mile_rate) + self.cost_to_park


class TransitTrip(Trip):
    def __init__(self, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time, fare_value):
        super().__init__(cn.TRANSIT_MODE, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time)
        self.fare_value = self.get_fare_value(fare_value) 
        self.cost = None

    def get_fare_value(self, fare_value):
        """
        TODO: check for zero/empty/NaN fare value. Set this to zero or standard fare value. 
        """
        if np.isnan(fare_value): 
            fare_value = 0
        return fare_value

    def set_cost(self):
        self.cost = self._calculate_cost(self.duration, self.fare_value)
        return self
        
    def _calculate_cost(self, duration, fare_value):
        self.cost = super()._calculate_base_cost(duration)
        return self.cost + fare_value
    
class BikeTrip(Trip):
    def __init__(self, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time, bike_rate=cn.BIKE_RATE):
        super().__init__(cn.BIKING_MODE, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time)
        self.bike_rate = bike_rate
        self.cost = None

    def set_cost(self):
        self.cost = self._calculate_cost(self.distance, self.duration, self.bike_rate)
        return self

    def _calculate_cost(self, distance, duration, bike_rate):
        self.cost = super()._calculate_base_cost(duration)
        return self.cost + (distance * bike_rate)
    

class WalkTrip(Trip):
    def __init__(self, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time):
        super().__init__(cn.WALKING_MODE, origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time)




