import init
import constants as cn
from index_base_class import IndexBaseClass
from trip import Trip

import pandas as pd



class ModeChoiceCalculator(IndexBaseClass):
    """
    
    """
    def __init__(self):
        pass

    def is_viable(self, trip):
        viable = 0
        if trip.mode == cn.CAR and trip.duration < 60:
            viable = 1
        elif trip.mode == cn.BIKE and trip.duration < 60:
            viable = 1
        elif trip.mode == cn.TRANSIT and trip.duration < 60:
            viable = 1
        elif trip.mode == cn.WALK and trip.duration < 45:
            viable = 1

            #can we take into account proximity? thinking of nearby locations with bad connections
            # or disnant locations with good connections. Most relevant for bus.

        #Make threasholds constants
        
        return viable

    
    def csv_to_dataframe(self, csv_filepath):
        df =pd.read_csv(csv_filepath)

        return df

    
    def extract_blkgrp(self, trip_id):
        blkgrp = trip_id.split('++')[0]

        return blkgrp

    
    def extract_dest(self, trip_id):
        dest = trip_id.split('++')[1]

        return dest


    def trip_from_row(self, row):
        """
        Given a dataframe with the available variables, create a trip class 
        with these variables
        """

        #Need to change strings for constants
        trip_id = row['trip_id']
        origin = self.extract_blkgrp(trip_id)
        destination = self.extract_dest(trip_id)
        mode = row['mode']
        distance = row['distance']
        duration = row['duration']
        basket_category = None
        pair = None
        #convert departure time to date-time object
        departure_time = row['departure_time']
        rank = None

        trip = Trip(trip_id, origin, destination, mode, distance, duration, basket_category, 
            pair, departure_time, rank)
        return trip

    
    def create_blockgroup_dict(self, df):

        """
        this function assumes that the df has a column for trip viability
        """
        blkgrp_dict = defaultdict(list)
        for index, row in df.iterrows():
            trip = self.trip_from_row(row)
            blkgrp = trip.origin
            viable= row['viable']
            #need a way to add viable to trip
            blkgrp_dict[blkgrp].append(trip)

        return blkgrp_dict


    def calculate_mode_avail(self, trips):
        """
        trips is a list of Trips

        """
        #make sure trip has viable attribute
        # Hours of data availability, HOURS constant should be float
        mode_avail = sum([trip.viable for trip in trips])
        mode_index = mode_aval/cn.HOURS #(?) name constant



    def calculate_availability(self, blkgrp):
        #for every block group
        # sum viability and divide by number of available hours
            #4 modes, 25 destnations, 12 hours
        #remaining number will be between 0-100 so we can classify into index



