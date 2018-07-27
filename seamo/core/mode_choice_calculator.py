import init
import constants as cn
from trip import BikeTrip, CarTrip, TransitTrip, WalkTrip
from index_base_class import IndexBase

import pandas as pd

from collections import defaultdict


class ModeChoiceCalculator(IndexBase):
    """
    
    """
    def __init__(self, car_time_threshold=cn.CAR_TIME_THRESHOLD,
                bike_time_threshold=cn.BIKE_TIME_THRESHOLD,
                transit_time_threshold=cn.TRANSIT_TIME_THRESHOLD,
                walk_time_threshold=cn.WALK_TIME_THRESHOLD):
        """
        Instantiate a ModeChoiceCalculator with different thresholds for the 
        four modes of transportation.
        Each threshold is a float denoting times in minutes.
        """

        self.car_time_threshold = car_time_threshold
        self.bike_time_threshold = bike_time_threshold
        self.transit_time_threshold = transit_time_threshold
        self.walk_time_threshold = walk_time_threshold


    def trip_from_row(self, row):
        """
        Given a row in a Pandas dataframe, instantiate a Trip object. 
        Depending on mode, return a subtype of Trip.
        Returns trip.
        """
        origin = row[cn.BLOCK_GROUP]
        dest_lat = row[cn.LAT]
        dest_lon = row[cn.LON]
    
        mode = row[cn.MODE]

        distance = row[cn.DISTANCE]
        duration = row[cn.DURATION]
        duration_in_traffic = [cn.DURATION_IN_TRAFFIC]
        fare_value = [cn.FARE_VALUE]

        basket_category = None

        # Need to convert departure time to date-time object
        departure_time = row[cn.DEPARTURE_TIME]
        
        trip = {cn.DRIVING_MODE: CarTrip(origin, dest_lat, dest_lon, departure_time, distance,
                                              duration, basket_category, duration_in_traffic=duration_in_traffic),
        cn.TRANSIT_MODE: TransitTrip(origin, dest_lat, dest_lon, departure_time, distance, duration,
                                          basket_category, fare_value=fare_value),
        cn.BIKING_MODE: BikeTrip(origin, dest_lat, dest_lon, departure_time, distance, duration,
                                      basket_category),
        cn.WALKING_MODE: WalkTrip(origin, dest_lat, dest_lon, departure_time, distance, duration,
                                       basket_category)}[mode]

        return trip


    def is_viable(self, trip):
        """
        Inputs:
            trip (Trip)
        Outputs:
            viable (int)
        
        This function takes in a Trip and returns a value indicating whether a
        trip is viable (1) or not viable (0).
        If the duration of a trip exceeds the threshold for that trip's mode,
        viability is 0. 
        """
        # TODO: time of day weight for different modes.
        # need to carry things?
        # elevation?

        viable = 0
        if trip.mode == cn.DRIVING_MODE and trip.duration < self.car_time_threshold:
            viable = 1
        elif trip.mode == cn.BIKING_MODE and trip.duration < self.bike_time_threshold:
            viable = 1
        elif trip.mode == cn.TRANSIT_MODE and trip.duration < self.transit_time_threshold:
            viable = 1
        elif trip.mode == cn.WALKING_MODE and trip.duration < self.walk_time_threshold:
            viable = 1

        # TODO: can we take into account proximity? thinking of nearby locations
        # with bad connections or disnant locations with good connections.
        # Most relevant for bus.
        
        return viable

    
    def trips_per_blockgroup(self, df, viable_only=False):
        """
        Inputs:
            df (Dataframe)
            viable_only (Boolean)
        Outputs:
            blkgrp_dict (dict)
        
        Given a dataframe containing data for one trip per row,  
        instantiate a trip for each row, calculate its viability,
        and aggregate the trips for each blockgroup.
    
        If viable_only == True, only append the viable trips to the lists. 

        Return a dict where keys are blockgroups and values are lists of Trips.
        """
        blkgrp_dict = defaultdict(list)
        for _, row in df.iterrows():
            trip = self.trip_from_row(row)
            blkgrp = trip.origin

            viable = self.is_viable(trip)
            trip.set_viability(viable)
            if viable_only:
                if viable == 1:
                    blkgrp_dict[blkgrp].append(trip)
            else:
                blkgrp_dict[blkgrp].append(trip)

        return blkgrp_dict


    def calculate_mode_avail(self, trips):
        """
        Input: trips (list of Trips)
        Output: mode index (float)
            for the list of trips as a function of viability

        This function assumes that each Trip in trips has a viability attribute
        """
        
        # Hours of data availability, HOURS constant should be float
        mode_avail = sum([trip.viable for trip in trips])
        
        # TODO: Update the calculation. We have different Trip types in trips.
        # 
        mode_index = mode_avail/cn.TRAVEL_HOURS #(?) name constant

        return mode_index


    def create_availability_csv(self, blkgrp_dict):
        """
        Takes in a blockgroup dictionary where blokgroups are keys and list of trips from
        that blockgroups are corresponding values, estimates the availability score for each blockroup
        and returns the csv with each block group's mobility score.

        """
        data = []
        for blkgrp, trips in blkgrp_dict.items():
            mode_index= calculate_mode_avail(trips)
            row={ cn.BLOCK_GROUP: blkgrp, cn.MODE_CHOICE_INDEX: mode_index}
            data.append(row)
        df = pd.DataFrame(data)

        df.to_csv(cn.MODE_CHOICE_FP)

