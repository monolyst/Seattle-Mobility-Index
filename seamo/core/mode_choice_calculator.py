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
        four modes of transportation, using defaults from constants.py.
        Each threshold is a float denoting times in minutes.
    
        To toggle a mode off (rule out that mode entirely), set its threshold to
        0. 
        """

        self.car_time_threshold = car_time_threshold
        self.bike_time_threshold = bike_time_threshold
        self.transit_time_threshold = transit_time_threshold
        self.walk_time_threshold = walk_time_threshold


    def trip_from_row(self, row):
        """
        Input:
            row: a row in a Pandas DataFrame
        Output:
            trip: a Trip object

        Given a row in a Pandas DataFrame containing attributes of a trip, 
        instantiate a Trip object. 
    
        Depending on the value for the column 'mode', return a subtype of Trip.
        """
        origin = row[cn.BLOCK_GROUP]
        dest_lat = row[cn.LAT]
        dest_lon = row[cn.LON]
    
        mode = row[cn.MODE]

        distance = row[cn.DISTANCE]
        duration = row[cn.DURATION]

        # TODO: find a way to not instantiate variables as None
        duration_in_traffic = self._handle_missing_columns(row, cn.DURATION_IN_TRAFFIC)
        fare_value = self._handle_missing_columns(row, cn.FARE_VALUE)

        basket_category = None

        departure_time = row[cn.DEPARTURE_TIME]

        dest_blockgroup = row[cn.DEST_BLOCK_GROUP]
        neighborhood_long = row[cn.NBHD_LONG]
        neighborhood_short = row[cn.NBHD_SHORT]
        council_district = row[cn.COUNCIL_DISTRICT]
        urban_village = row[cn.URBAN_VILLAGE]
        zipcode = row[cn.ZIPCODE]

        # Create a subclass of Trip based on the mode
        if mode == cn.DRIVING_MODE:
            trip = CarTrip(origin, dest_lat, dest_lon, distance, duration,
                           basket_category, departure_time,
                           duration_in_traffic=duration_in_traffic)
        elif mode == cn.TRANSIT_MODE:
            trip = TransitTrip(origin, dest_lat, dest_lon, distance, duration,
                               basket_category, departure_time,
                               fare_value=fare_value)
        elif mode == cn.BIKING_MODE:
            trip = BikeTrip(origin, dest_lat, dest_lon, distance, duration,
                            basket_category, departure_time)
        elif mode == cn.WALKING_MODE:
            trip = WalkTrip(origin, dest_lat, dest_lon, distance, duration,
                            basket_category, departure_time)
        else:
            # Should have a custom exception here
            trip = None
        trip.set_geocoded_attributes(dest_blockgroup, neighborhood_long,
            neighborhood_short, council_district, urban_village, zipcode)    
        return trip


    def _handle_missing_columns(self, row, attribute):
        try:
            row[attribute]
        except:
            return None
        else:
            return row[attribute]            


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
            # If the trip's fare_value is None, Google Maps gave walking directions
            # and thus, transit is not viable.
            if trip.fare_value:
                viable = 1
        elif trip.mode == cn.WALKING_MODE and trip.duration < self.walk_time_threshold:
            viable = 1

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
        Output: scores (dict)
                    keys: blockgroup IDs (int)
                    values: list of Trip objects 

        For each mode, calculate the ratio of viable trips to total trips for 
        that particular mode. Return a dict containing scores for each mode.

        """
        # Hours of data availability, HOURS constant should be float
        scores = {}
        for mode in [cn.DRIVING_MODE, cn.BIKING_MODE, cn.TRANSIT_MODE, cn.WALKING_MODE]:
            # List of 0s and 1s corresponding to binary viability value for each trip
            viability_per_trip = [trip.viable for trip in trips if trip.mode == mode]

            # Number of viable trips
            viable_trips = sum(viability_per_trip)
            mode_avail_score = viable_trips / len(viability_per_trip)

            # if mode == cn.DRIVING_MODE or mode == cn.TRANSIT_MODE:
            #    mode_avail /= cn.TRAVEL_HOURS
            # mode_avail /= cn.BASKET_SIZE
            
            scores[mode] = mode_avail_score
        return scores 
        

    def create_availability_df(self, blkgrp_dict):
        """
        Input:
            blkgrp_dict (dict)
                keys: blockgroup IDs (int)
                values: list of Trips originating from that blockgroup
        Output:
            df (Pandas DataFrame)

        Given a dict in which keys are blockgroup IDs and values are a list of
        trips from that blockgroup, this method calculates a mode availability 
        score for each blockroup and creates a Pandas DataFrame with a row for 
        each block group and columns for mode-specific and total availability
        scores. 

        Mode-specific scores are calculated by the ratio of viable trips to
        total trips. The final mode availability score is the unweighted mean 
        of the 4 mode-specific scores. 
        """
        data = []
        for blkgrp, trips in blkgrp_dict.items():
            mode_scores = self.calculate_mode_avail(trips)
            row = mode_scores
            mode_index = sum(mode_scores.values()) / 4
            row[cn.BLOCK_GROUP] =  blkgrp
            row[cn.MODE_CHOICE_INDEX] = mode_index
            data.append(row)
            
        cols=[cn.BLOCK_GROUP, cn.DRIVING_MODE, cn.BIKING_MODE, cn.TRANSIT_MODE,
              cn.WALKING_MODE, cn.MODE_CHOICE_INDEX]

        df = pd.DataFrame(data, columns=cols)
    
        return df

