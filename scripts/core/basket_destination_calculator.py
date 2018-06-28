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
from pandas.io.json import json_normalize
from urllib.request import Request, urlopen  # Python 3

DATADIR = os.path.join(os.getcwd(), "../../seamo/data/raw")
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles

DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
UNITS = 'imperial'
MODE = 'driving'
# API_KEY = open(os.path.join(BASEDIR, "api-key.txt"), 'r').read()

def calculate_distance_to_basket(blockgroup, origin_lat, origin_long):
    """Calculate the distance (and travel time) to each destination
    and produce a CSV file of the data.
    This calls the Google Matrix API

    Inputs:

    Output:
    
    Side effects: produces file with distances.

    """ 
    destinations_df = pd.read_csv(os.path.join(DATADIR, data_path)) 

    min_lat = origin_lat - PROXIMITY_THRESHOLD
    max_lat = origin_lat + PROXIMITY_THRESHOLD
    min_long = origin_long - PROXIMITY_THRESHOLD
    max_long = origin_long + PROXIMITY_THRESHOLD
    
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

        url = DIST_MATRIX_URL +\
              'units={0}'.format(UNITS) +\
              '&mode={0}'.format(MODE) +\
              '&origins={0}'.format(origin) +\
              "&destinations={0}".format(destination) +\
              "&key={0}".format(API_KEY)
        q = Request(url)
        a = urlopen(q).read()
        data = json.loads(a)

        if 'errorZ' in data:
            print (data["error"])
        
        # All this work just to get a single number! dang. 
        # message for AP; what does json normalize do, and why we need df?
        # the thing appended to distance is a number.. why is it a list?
        df = json_normalize(data['rows'][0]['elements'])  
        df['distance.value'] = df['distance.value']/1609
        distance.append(df['distance.value'].tolist()[0])    
        
    destinations_df['distance'] = distance
    destinations_df['origin'] = blockgroup 
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
                "post_office",
                "school",
                "cafe"]
 
    # filter destination based on rank (distance from destination)
    # There is probably a better way to do this in pandas.
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
