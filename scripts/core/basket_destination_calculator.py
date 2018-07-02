# coding: utf-8
"""
Basket Destination Calculator
 
This script constructs a market basket of destinations relevant to people 
who travel in Seattle. The basket may include collections of trips to 
nearby points of interest and activity centers that are specific to 
each origin, and a collection of trips to citywide destinations 
that are the same for all starting points.  

https://public.tableau.com/views/Basket_of_Destinations/Dashboard?:embed=y&:display_count=yes

This script accesses the Google Map Distance Matrix API to rank 
each possible origin-destination by their driving distance. 
The basket definition is created by using parameters to filter each class of destination.
"""

import json
import os

import numpy as np
import pandas as pd
from urllib.request import Request, urlopen  # Python 3

DATADIR = os.path.join(os.getcwd(), "../../seamo/data/raw")
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles
METERS_TO_MILES = 1609


# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
UNITS = 'imperial'
MODE = 'driving'

# Google API naming
PLACE_LAT = 'lat'
PLACE_LON = 'lng' # why not lon ugh
PLACE_CLASS = 'class'
PLACE_RANK = 'rank'

DISTANCE = 'distance'
PAIR = 'pair'


# Seattle Census Data naming
CENSUS_LAT = 'CT_LAT'
CENSUS_LON = 'CT_LON'
BLOCKGROUP = 'BLOCKGROUP'

class BasketCalculator:
    def __init__(self, api_key):
        self.api_key = api_key


    def origins_to_distances(self, origins_fp, dest_fp):
        origins = pd.read_csv(origins_fp)
        destinations = pd.read_csv(dest_fp)
        dist_matrix = [] 
        for i, row in origins:
            blockgroup = row[BLOCKGROUP]
            origin_lat = row[CENSUS_LAT]
            origin_lon = row[CENSUS_LON]
            # Filter for distance
            filtered_dests = self.filter_destinations(destinations)
            distances = self.calculate_distance_to_basket(origin_lat, origin_lon, filtered_dests) 
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
        Sort and rank for distance by class
        Input: dataframe
        Output: dataframe with an added 'rank' column
        """
        dist_df[PLACE_RANK] = dist_df.groupby([PLACE_CLASS])[DISTANCE].rank(ascending=True)
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

        q = Request(url)
        a = urlopen(q).read()
        response = json.loads(a)

        if 'errorZ' in response:
            # Do we really want to print this?  
            print (response["error"])
        
        distance = response['rows'][0]['elements'][0]['distance']['value']

        return distance 


    def calculate_distance_to_basket(self, origin_lat, origin_lon, destinations):
        """Calculate the distance (and travel time) to each destination
        and produce a CSV file of the data.
        This calls the Google Matrix API.

        Inputs:
            origin_lat (float)
            origin_lon (float)
            destinations (DataFrame)
        Output:
            distances (dict)

        """ 
        distances = {}
        
        for index, row in destinations.iterrows():
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
        categories = ["urban_village",
                    "destination park",
                    "supermarket",
                    "library",
                    "hospital",
                    "pharmacy",
                    "post_office",
                    "school",
                    "cafe"]
     
        # filter destination based on rank (distance from destination)
        # There is probably a better way to do this in pandas.
        # Why not just.. keep everything above 20
        # And if it's not a citywide, cut it to 5
        dest_df = dest_df[dest_df.rank <= 20]
        dest_df = dest_df[(dest_df[PLACE_CLASS] != "citywide") | (dest_df['rank'] <= 20)]

        return_df


if __name__ == "__main__":
    """
    Ask the user for their API key.
    """
    api_key = input("Enter your Google API key: ")
    basket_calculator = BasketCalculator(api_key)
    
    # THIS DOES NOT WORK YET
    origins_fp = os.path.join(DATATDIR, filepath)
    destinations_fp = os.path.join(DATADIR, filepath)

    distance_df = basket_calculator.origins_to_distances(origins_fp, destinations_fp)
    
    distance_df.to_csv(path)
    # filter it
    basket_calculator.filter_by_rank(path)

    # When shall the file names be specified?

    # Export to csv
    #if os.path.exists(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')):
    #    destinations_df.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='a', header=False, index=False)
    #else:
    #    destinations_df.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='w', header=True, index=False)
