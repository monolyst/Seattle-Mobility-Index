# coding: utf-8
"""
Basket Destination Calculator
 
This script constructs a market basket of destinations relevant to people 
who travel in Seattle. The basket may nearby points of interest and activity 
centers that are specific to each origin, and citywide destinations 
that are the same for all starting points.  

https://public.tableau.com/views/Basket_of_Destinations/Dashboard?:embed=y&:display_count=yes

This script accesses the Google Map Distance Matrix API and ranks each 
possible origin-destination pair by their driving distance. 
The basket definition is created by using parameters to filter each 
class of destination.
"""

import json
import os
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

DATADIR = os.path.join(os.getcwd(), "../../seamo/data/raw")
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles
METERS_TO_MILES = 1609

# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
UNITS = 'imperial'
MODE = 'driving'

# Google API naming
PLACE_LAT = 'lat'
PLACE_LON = 'lng' 
PLACE_CLASS = 'class'
PLACE_RANK = 'rank'

DISTANCE = 'distance'
PAIR = 'pair'

# Seattle Census Data naming
CENSUS_LAT = 'CT_LAT'
CENSUS_LON = 'CT_LON'
BLOCKGROUP = 'BLOCKGROUP'

ORIGIN_FP = os.path.join(DATADIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv') 
DEST_FP = os.path.join(DATADIR, 'GoogleMatrix_Places_Full.csv') 


class BasketCalculator:

    origin_df = pd.read_csv(ORIGIN_FP)
    dest_df = pd.read_csv(DEST_FP)

    def __init__(self, api_key):
        self.api_key = api_key


    def origins_to_distances(self, 
            origin_df=origin_df,
            dest_df=dest_df):
        dist_matrix = [] 
        for i, row in origin_df.iterrows():
            blockgroup = row[BLOCKGROUP]
            origin_lat = row[CENSUS_LAT]
            origin_lon = row[CENSUS_LON]
            # Filter for distance
            filtered_df = self.filter_destinations(origin_lat, origin_lon, dest_df)
            distances = self.calculate_distance_to_basket(origin_lat, origin_lon, filtered_df) 
            for place_id, data in distances:
                distance = data[DISTANCE]
                dest_class = data[PLACE_CLASS]
                pair = "{0}-{1}".format(blockgroup, place_id) 
                dist_matrix.append([pair, distance, dest_class])

        dist_df = pd.DataFrame(dist_matrix, columns=[PAIR, DISTANCE, PLACE_CLASS])
    
        # rank it
        dist_df = self.rank_destinations(dist_df)

        return dist_df 


    def rank_destinations(self, dist_df):
        """
        For each blockgroup, rank destinations by class for proximity
        Input: dataframe
        Output: dataframe with an added 'rank' column
        """
        # Group by blockgroup and destination class
        grouped = dist_df.groupby([BLOCKGROUP, PLACE_CLASS])
        # Rank by proximity (closest is highest) 
        dist_df[PLACE_RANK] = grouped[DISTANCE].rank(
            ascending=True, method='first')
        return dist_df


    def filter_destinations(self, origin_lat, origin_lon, dest_df):
        """
        Filter general destinations for proximity within a threshold. 
        Keep all citywide and urban_village (why the latter?) 
        Input: origin_lat, origin_lon, destinations dataframe
        Output: dataframe
        """
        min_lat = origin_lat - PROXIMITY_THRESHOLD
        max_lat = origin_lat + PROXIMITY_THRESHOLD
        min_long = origin_lon - PROXIMITY_THRESHOLD
        max_long = origin_lon + PROXIMITY_THRESHOLD

        dest_df = dest_df[(dest_df['class'] == "citywide") | 
                        (dest_df['class'] == "urban_village") | 
                        (
                        (dest_df['lat'] > min_lat) & (dest_df['lat'] < max_lat) &
                        (dest_df['lng'] > min_long) & (dest_df['lng'] < max_long)
                        )
                         ]
        return dest_df
        

    def calculate_distance(self, origin, destination):
        """
        Input: origin string, destination string
        Output: distance in miles
        Calls Google Matrix API
        """ 
        # Do we need to throw an exception here if this don't work
        url = DIST_MATRIX_URL +\
              'units={0}'.format(UNITS) +\
              '&mode={0}'.format(MODE) +\
              '&origins={0}'.format(origin) +\
              "&destinations={0}".format(destination) +\
              "&key={0}".format(api_key)

        request = Request(url)
        try: 
            response = urlopen(request).read()
        except:
            pass
        # if status OK
        # if status REQUEST_DENIED

        # types of errors: "error_message"
        # rows [elements][0][status] NOT_FOUND
        data = json.loads(response)

        distance = data['rows'][0]['elements'][0]['distance']['value']

        return distance 


    def calculate_distance_to_basket(self, origin_lat, origin_lon, dest_df):
        """Calculate the distance (and travel time) to each destination
        and produce a CSV file of the data.
        This calls the Google Matrix API.

        Inputs:
            origin_lat (float)
            origin_lon (float)
            dest_df (DataFrame)
        Output:
            distances (dict)

        """ 
        distances = {}
        
        for index, row in dest_df.iterrows():
            dest_lat = row[PLACE_LAT]
            dest_lon = row[PLACE_LON] 
            dest_class = row[PLACE_CLASS]
    
            place_id = row['place_id']
            # Build the origin and destination strings
            origin = str(origin_lat) + "," + str(origin_lon)
            destination = str(dest_lat) + "," + str(dest_lon)

            distance = self.calculate_distance(origin, destination)

            # Store the distance and the class 
            distances[place_id] = { DISTANCE: distance,
                                    PLACE_CLASS: dest_class }

        return distances


    def filter_by_rank(dest_df):
        """
        Filter the universe of baskets to match parameter limits. 
        This will reduce the size of the table to make it easier for analysis and 
        geocoding. 
        """
        dest_df = dest_df[dest_df.rank <= 20]
        dest_df = dest_df[(dest_df[PLACE_CLASS] != "citywide") | (dest_df['rank'] <= 20)]

        return_df


if __name__ == "__main__":
    """
    Ask the user for their API key.
    """
    api_key = input("Enter your Google API key: ")
    basket_calculator = BasketCalculator(api_key)

    # Should this actually take dataframes, not files?
    origin_df = BasketCalculator.origin_df
    dest_df = BasketCalculator.dest_df
    distance_df = basket_calculator.origins_to_distances(origin_df, dest_df)
    
    # Put out to a CSV file
    # distance_df.to_csv(path)
    # basket_calculator.filter_by_rank(path)
