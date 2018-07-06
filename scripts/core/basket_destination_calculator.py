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
            # Filter for proximity 
            filtered_df = self.filter_destinations(origin_lat, origin_lon, dest_df)
            distances = self.calculate_distance_to_basket(origin_lat, origin_lon, filtered_df) 
            for place_id, data in distances.items():
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
        min_lon = origin_lon - PROXIMITY_THRESHOLD
        max_lon = origin_lon + PROXIMITY_THRESHOLD

        dest_df = dest_df[(dest_df[PLACE_CLASS] == "citywide") | 
                        (dest_df[PLACE_CLASS] == "urban_village") | 
                        ((dest_df[PLACE_LAT] > min_lat) & (dest_df[PLACE_LAT] < max_lat) &
                        (dest_df[PLACE_LON] > min_lon) & (dest_df[PLACE_LON] < max_lon)
                        )
                        ]
        return dest_df
        

    def calculate_distance(self, origin, destination):
        """
        Input: origin string, destination string
        Output: distance in miles
        Calls Google Matrix API
        """ 
        distance = None

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
            raise Exception("Couldn't open link.")  
            # Do we want to try again, or just skip it?
            # Should I say 'return distance' or None for clarity?
            return None 

        data = json.loads(response)

        if data['status'] != 'OK':
            message = data['error_message']
            raise Exception(message)
            # Going to make a SeamoError type.
        else:
            elements = data['rows'][0]['elements']
            element = elements[0]
            if element['status'] == 'NOT_FOUND':
                # If the origin-destination pair is not found, should write to a log.
                raise Exception('No good.')  
                return distance 
            elif element['status'] == 'OK':
                distance = element['distance']['value']

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
            if distance:
                # Store the distance and the class 
                distances[place_id] = { DISTANCE: distance,
                                        PLACE_CLASS: dest_class }

        return distances

    def create_basket(self, basket_combination):
        """
        Given a list of integers denoting counts for basket categories 
        create a basket of destinations for a blockgroup. 
        Input: basket_combination (list)
        Output: dataframe
        """
        # We assume that the ranks are for a blockgroup.
        for i in range(len(CLASS_LIST)):
                filtered_data = filtered_data[(filtered_data[PLACE_CLASS] != CLASS_LIST[i]) | (filtered_data[PLACE_RANK] <= basket_combination[i])]
        # Does this take in ONE blockgroup, or the whole df of blockgroups?
        # output: the basket. top N locations per category

        # also need to work out cloud storage for the DF that comes out


if __name__ == "__main__":
    """
    Ask the user for their API key.
    """
    api_key = input("Enter your Google API key: ")
    basket_calculator = BasketCalculator(api_key)

    origin_df = BasketCalculator.origin_df
    dest_df = BasketCalculator.dest_df

    distance_df = basket_calculator.origins_to_distances(origin_df, dest_df)
    # Is it a problem that this is all stored in memory until finally put it out    

    output_fp = "basket.csv"
    distance_df.to_csv(output_fp)
    # Import Darius csv to sql code
    # Output to sql.
