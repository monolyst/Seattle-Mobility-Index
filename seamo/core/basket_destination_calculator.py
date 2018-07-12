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
import __init__
import json
import os
from urllib.request import Request, urlopen

import constants as cn
import pandas as pd

DATADIR = os.path.join(os.getcwd(), "../../seamo/data/raw")
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles
METERS_TO_MILES = 1609

# Google API naming
PLACE_LAT = 'lat'
PLACE_LON = 'lng' 
PLACE_CLASS = 'class'
PLACE_RANK = 'rank'

DISTANCE = 'distance'
PAIR = 'pair'

# Seattle Census Data naming

ORIGIN_FP = os.path.join(DATADIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv') 
DEST_FP = os.path.join(DATADIR, 'GoogleMatrix_Places_Full.csv') 

class BasketCalculator:

    origin_df = pd.read_csv(ORIGIN_FP)
    dest_df = pd.read_csv(DEST_FP)

    def __init__(self, api_key):
        """
        Initialize BasketCalculator with an API key. 
        
        Inputs: api_key (string)
        """
        self.api_key = api_key


    def origins_to_distances(self, origin_df=origin_df, dest_df=dest_df):
        """
        For every origin, store the distance to every destination in the 
        full basket of destinations. Distance is calculated via the Google
        Distance Matrix API.

        Inputs: origin_df (dataframe), dest_df (dataframe)
        Outputs: dist_df (dataframe)
        
        """
        dist_matrix = [] 
        for i, row in origin_df.iterrows():
            blockgroup = row[cn.BLOCKGROUP]
            origin = Coordinate(row[cn.CENSUS_LAT], row[cn.CENSUS_LON])
            distances = self.calculate_distance_to_basket(origin, dest_df) 
            for place_id, data in distances.items():
                distance = data[cn.DISTANCE]
                dest_class = data[cn.CLASS]
                pair = "{0}-{1}".format(blockgroup, place_id) 
                dist_matrix.append([pair, distance, dest_class])

        dist_df = pd.DataFrame(dist_matrix, columns=[PAIR, DISTANCE, PLACE_CLASS])
    
        # rank it by proximity
        dist_df = self.rank_destinations(dist_df)

        return dist_df 


    def rank_destinations(self, dist_df):
        """
        For each blockgroup, rank destinations by class for proximity.

        Input: dataframe
        Output: dataframe with an added 'rank' column
        """
        # Group by blockgroup and destination class
        grouped = dist_df.groupby([cn.BLOCKGROUP, PLACE_CLASS])
        # Rank by proximity (closest is highest) 
        dist_df[PLACE_RANK] = grouped[DISTANCE].rank(
            ascending=True, method='first')
        return dist_df


    def calculate_distance(self, origin, destination):
        """
        Calculate the distance between an origin and destination pair.
        Calls Google Distance Matrix API.
    
        Input:  origin (Coordinate)
                destination (Coordinate)
        Output: distance in miles (int)
        """ 
        distance = 0 

        url = cn.DIST_MATRIX_URL +\
              'units={0}'.format(cn.IMPERIAL_UNITS) +\
              '&mode={0}'.format(cn.DRIVING_MODE) +\
              '&origins={0}'.format(str(origin)) +\
              "&destinations={0}".format(str(destination)) +\
              "&key={0}".format(api_key)
        request = Request(url)
        try: 
            response = urlopen(request).read()
        except:
            raise Exception("Couldn't open link.")  

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
                raise Exception('Could not find the distance for that pair.')  
            elif element['status'] == 'OK':
                distance = element['distance']['value']

        return distance 


    def calculate_distance_to_basket(self, origin, dest_df):
        """Calculate the distance (and travel time) to each destination
        and produce a CSV file of the data.
        This calls the Google Matrix API.

        Inputs:
            origin (Coordinate)
            dest_df (DataFrame)
        Output:
            distances (dict)

        """ 
        distances = {}

        for index, row in dest_df.iterrows():
            destination = Coordinate(row[PLACE_LAT], row[PLACE_LON])
            dest_class = row[PLACE_CLASS]
            #TODO: Replace with constant when that is merged into master.
            place_id = row['place_id']

            distance = self.calculate_distance(origin, destination)
            if distance:
                # Store the distance and the class of destination
                distances[place_id] = { DISTANCE: distance,
                                        PLACE_CLASS: dest_class }

        return distances


    def create_basket(self, origin_df, basket_combination):
        """
        Given a list of integers denoting counts for basket categories 
        and a dataframe of origins (blockgroups), create a basket of destinations 
        for each blockgroup. 

        Input: origin_df (dataframe), basket_combination (list)
        Output: dataframe
        """

        for i in range(len(CLASS_LIST)):
            origin_df = origin_df[(origin_df[PLACE_CLASS] != CLASS_LIST[i]) | 
                (origin_df[PLACE_RANK] <= basket_combination[i])]

        return origin_df

if __name__ == "__main__":
    """
    Ask the user for their API key.
    """
    api_key = input("Enter your Google API key: ")
    basket_calculator = BasketCalculator(api_key)

    origin_df = BasketCalculator.origin_df
    dest_df = BasketCalculator.dest_df

    distance_df = basket_calculator.origins_to_distances(origin_df, dest_df)
    # Is it a problem that this is all stored in memory until write to file?    

    output_fp = "basket.csv"
    distance_df.to_csv(output_fp)
    # Import Darius csv to sql code
    # Output to sql.
