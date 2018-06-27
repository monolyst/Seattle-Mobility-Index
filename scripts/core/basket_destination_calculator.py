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

import itertools
import json
import math
import os
import time
import string
from datetime import datetime

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from sklearn.metrics import mean_squared_error
from urllib.request import Request, urlopen  # Python 3

DATADIR = os.path.join(os.getcwd(), "../seamo/data/raw")
DIST_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&mode=driving&origins="
# ANALYSISDIR = os.path.join(BASEDIR, "Analysis")
# API_Key = open(os.path.join(BASEDIR, "api-key.txt"), 'r').read()

#def calculate_distance_to_basket(data_path='GoogleMatrix_Places_Full.csv', origin, origin_lat, origin_long):
def calculate_distance_to_basket(data_path, origin_lat, origin_long):
    """Calculate the distance (and travel time) to each destination
    and produce a CSV file of the data.
    This calls the Google Matrix API

    Inputs:

    Output:
    
    Side effects: produces file with distances.

    """ 
    destinations_df = pd.read_csv(os.path.join(DATADIR, data_path)) 

    min_lat = origin_lat - .8
    max_lat = origin_lat + .8
    min_long = origin_long - .8
    max_long = origin_long + .8
    
    # Filter general destinations that are approximately less than 5-6 miles away 
    destinations_df = destinations_df[(destinations_df['class'] == "citywide") | 
                                    (destinations_df['class'] == "urban_village") | 
                                    (
                                    (destinations_df['lat'] > min_lat) & (destinations_df['lat'] < max_lat) &
                                    (destinations_df['lng'] > min_long) & (destinations_df['lng'] < max_long)
                                    )
                                     ]
    distance = []
    
    for index, row in destinations_df.iterrows():
        # Build the origin and destination strings
        origin = str(origin_lat) + "," + str(origin_long)
        destination = str(row["lat"]) + "," + str(row["lng"])
        url = DIST_MATRIX_URL + origin + "&destinations" + destination + "&key" + API_KEY
        q = Request(URL)
        a = urlopen(q).read()
        data = json.loads(a)

        if 'errorZ' in data:
            print (data["error"])
        
        df = json_normalize(data['rows'][0]['elements'])  
        df['distance.value'] = df['distance.value']/1609
        distance.append(df['distance.value'].tolist()[0])    
        
    destinations_df['distance'] = distance
    destinations_df['origin'] = origin
    destinations_df['pair'] = destinations_df['origin'].astype(str)  + "-" + destinations_df['place_id'].astype(str)
    
    # Sort and rank by class
    destinations_df['rank'] = destinations_df.groupby(['class'])['distance'].rank(ascending=True)

    # Export to csv
    if os.path.exists(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')):
        destinations_df.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='a', header=False, index=False)
    else:
        destinations_df.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='w', header=True, index=False)


def evaluate_proximity_ratio(destination_data_path):
    """
    Filter the universe of baskets to match parameter limits. 
    This will reduce the size of the table to make it easier for analysis and 
    geocoding. 
    """
    destinations_df = pd.read_csv(destination_data_path) 
   
    categories = ["urban_village",
                "destination park",
                "supermarket",
                "library",
                "hospital",
                "pharmacy",
                "post_office", # why underscore and others not?
                "school",
                "cafe"]
 
    # filter destination based on rank (distance from destination)
    destinations_df = destinations_df[(destinations_df['class'] != "urban village") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "citywide") | (destinations_df['rank'] <= 20)]
    destinations_df = destinations_df[(destinations_df['class'] != "destination park") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "supermarket") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "library") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "hospital") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "pharmacy") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "post_office") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "school") | (destinations_df['rank'] <= 5)]
    destinations_df = destinations_df[(destinations_df['class'] != "cafe") | (destinations_df['rank'] <= 5)]

    destinations_df.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv', mode='w', header=True, index=False))


if __name__ == "__main__":
    destination_data_path = os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv') 
    evaluate_proximity_ratio(destination_data_path)
