# coding: utf-8

# ## Basket Destination Calculator
# 
# The purpose of this script is to construct a market basket of destinations relevant to people who travel in Seattle. The basket may include collections of trips to nearby points of interest and activity centers that are specific to each origin, and a collection of trips to citywide destinations that are the same for all starting points. 
# 

# 
# https://public.tableau.com/views/Basket_of_Destinations/Dashboard?:embed=y&:display_count=yes
# 
# This script accesses the Google Map Distance Matrix API to rank each possible origin-destination by their driving distance. The basket definition is created by using parameters to filter each class of destination.

import pandas as pd
import numpy as np
import os
from pandas.io.json import json_normalize
import json
from datetime import datetime
import os.path
import time
import math
from sklearn.metrics import mean_squared_error

try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2
    
import string
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

DATADIR = os.path.join(os.getcwd(), "../seamo/data/raw")
# We don't have this yet..
# ANALYSISDIR = os.path.join(BASEDIR, "Analysis")

# We don't have this
# API_Key = open(os.path.join(BASEDIR, "api-key.txt"), 'r').read()

# ## Combine google places with citywide places for a full list of destinations

# Combine Google places data with citywide places. The citywide file contain urban villages, destination parks, and 
# citywide points.
df_Places_Google = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places.csv'))
#df_Places_Citywide = pd.read_csv('GoogleMatrix_Places_Citywide.csv')
#df_Places_Full = pd.concat([df_Places_Google,df_Places_Citywide])
#df_Places_Full.to_csv("GoogleMatrix_Places_Full.csv", mode='w', header=True, index=False)

# Calculate the distance (and travel time) to each destination 
def distanceToBasket(origin, originLat, originLong):
    dfDestinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Full.csv') 

    minLat = originLat - .8
    maxLat = originLat + .8
    minLng = originLong - .8
    maxLng = originLong + .8
    
    # filter general destinations that are approximately less than 5-6 miles away 
    dfDestinations = dfDestinations[(dfDestinations['class'] == "citywide") | 
                                    (dfDestinations['class'] == "urban village") | 
                                    (
                                    (dfDestinations['lat'] > minLat) & (dfDestinations['lat'] < maxLat) &
                                    (dfDestinations['lng'] > minLng) & (dfDestinations['lng'] < maxLng)
                                    )
                                     ]
                                     
    Distance = []
    
    for index, row in dfDestinations.iterrows():

        # Build the Origin and Destination strings
        Origin = str(originLat) + "," + str(originLong)
        Destination = str(row["lat"]) + "," + str(row["lng"])
        URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&mode=driving&origins=" + Origin +                      "&destinations=" + Destination + "&key=" + API_Key
        #print (URL)
        q = Request(URL)
        a = urlopen(q).read()
        data = json.loads(a)

        if 'errorZ' in data:
            print (data["error"])
        
        df = json_normalize(data['rows'][0]['elements'])  
        df['distance.value'] = df['distance.value']/1609
        Distance.append(df['distance.value'].tolist()[0])    
        
     #   print (df)  
    dfDestinations['distance'] = Distance
    dfDestinations['origin'] = origin
    dfDestinations['pair'] = dfDestinations['origin'].astype(str)  + "-" + dfDestinations['place_id'].astype(str)
    
    # Sort and rank by class
    dfDestinations['rank'] = dfDestinations.groupby(['class'])['distance'].rank(ascending=True)
    
    
    # Export to csv
    if os.path.exists(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'))
        dfDestinations.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='a', header=False, index=False)
    else:
        dfDestinations.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'), mode='w', header=True, index=False)

# ## Call google distance matrix API

# load the list of origins and call the distance to basket function for each origin
dfOrigins = pd.read_csv(os.path.join(DATADIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv'))

dfOrigins = dfOrigins[
                    (dfOrigins['BLOCKGROUP'] == 530330062001) |
                      (dfOrigins['BLOCKGROUP'] == 530330030003) |
                      (dfOrigins['BLOCKGROUP'] == 530330068002) |
                    (dfOrigins['BLOCKGROUP'] == 530330107012) |
                      (dfOrigins['BLOCKGROUP'] == 530330077003)
]

for index, row in dfOrigins.iterrows():
    print (row['BLOCKGROUP'])
    distanceToBasket(row['BLOCKGROUP'],row['CT_LON'],row['CT_LAT'])
    
# Filter the universe of baskets to match parameter limits. This will reduce the size of the table to make it easier
# for analysis and geocoding 

def distilleBasketPrelim():

    df_destinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')) 
    
    # filter destination based on rank (distance from destination)
    df_destinations = df_destinations[(df_destinations['class'] != "urban village") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "citywide") | (df_destinations['rank'] <= 20)]
    df_destinations = df_destinations[(df_destinations['class'] != "destination park") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "supermarket") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "library") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "hospital") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "pharmacy") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "post_office") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "school") | (df_destinations['rank'] <= 5)]
    df_destinations = df_destinations[(df_destinations['class'] != "cafe") | (df_destinations['rank'] <= 5)]

    df_destinations.to_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv', mode='w', header=True, index=False))
    
distilleBasketPrelim()  

# ## Tune and Evaluate Model
# We will evaluate the model by comparing the 'proximity ratio' from the results with the ratio from the PSRC survey for each block group. We will look at all possible parameter calculations and identify the ones with the lowest scores.
# 
# We can compare results with the Puget Sound Regional Household Travel Survey. However, keep in mind that survey techniques incorporate behavior biases, such as those based on income, job status, etc. But our universal basket of destinations is based on opportunity, for which we do not want to start with different basket for different people. This does not preclude the use of weighting coefficients that could tune baskets for different income levels or types of households. 

# construct the basket for each blockgroup, calculate the proximity ratio, and compare it with sample results from
# the PSRC survey

def distilleBasketTest(testArray):
    
    global df_sample 
    global df_destinations
    
    # filter to match basket parameters based on rank (distance from destination)
    df_destinations = df_destinations[(df_destinations['class'] != "urban village") | (df_destinations['rank'] <= testArray[0])]
    df_destinations = df_destinations[(df_destinations['class'] != "citywide") | (df_destinations['rank'] <= testArray[1])]
    df_destinations = df_destinations[(df_destinations['class'] != "destination park") | (df_destinations['rank'] <= testArray[2])]
    df_destinations = df_destinations[(df_destinations['class'] != "supermarket") | (df_destinations['rank'] <= testArray[3])]
    df_destinations = df_destinations[(df_destinations['class'] != "library") | (df_destinations['rank'] <= testArray[4])]
    df_destinations = df_destinations[(df_destinations['class'] != "hospital") | (df_destinations['rank'] <= testArray[5])]
    df_destinations = df_destinations[(df_destinations['class'] != "pharmacy") | (df_destinations['rank'] <= testArray[6])]
    df_destinations = df_destinations[(df_destinations['class'] != "post_office") | (df_destinations['rank'] <= testArray[7])]
    df_destinations = df_destinations[(df_destinations['class'] != "school") | (df_destinations['rank'] <= testArray[8])]
    df_destinations = df_destinations[(df_destinations['class'] != "cafe") | (df_destinations['rank'] <= testArray[9])]
    
    # aggregate block group trips
    # proximity ration = trips under 2 miles vs trips between 2 and 10 miles
    df_destinations['dist_under_2'] = np.where(df_destinations['distance'] < 2.0,1,0)
    df_destinations['dist_2_to_10'] = np.where((df_destinations['distance']>=2) & (df_destinations['distance']<10.0),1,0)
    df_blockgroup = df_destinations.groupby(['origin'], as_index=False).agg({'dist_under_2':sum,'dist_2_to_10':sum})
    df_blockgroup['proximity_ratio_test'] = df_blockgroup['dist_under_2']/df_blockgroup['dist_2_to_10']
 
    print (df_blockgroup)
    # merge with evaluation file
    df_merged = pd.merge(left=df_blockgroup, right=df_sample, how='left', left_on='origin', right_on='bg_origin')
    df_merged = df_merged.dropna()
    
    # evaluate results for this test array
    target = df_merged['proximity_ratio']
    predictions = df_merged['proximity_ratio_test']
    mse = mean_squared_error(target, predictions)

    return (mse)

df_sample = pd.read_csv(os.path.join(DATADIR, 'Proximity_Ratio.csv')) 
df_destinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')) 

testArray = [2,11,3,2,2,2,1,0,1,2]
distilleBasketTest(testArray)


## Brute force function to evaluate all combinations. There are 200,000 possible combinations.

import itertools

df_sample = pd.read_csv(os.path.join(DATADIR, 'Proximity_Ratio.csv')) 
df_destinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')) 

df_basketCombinations = pd.DataFrame()


sizeLimit = 25

# Define parameter domain
AA = [0,1,2,3,4] # urban village
BB = [8,9,10,11,12,13] # citywide destination
A = [0,1,2,3] # destination park
B = [0,1,2,3] # supermarket
C = [0,1,2,3] # library
D = [0,1,2,3] # hospital
E = [0,1,2,3] # pharmacy
F = [0,1,2,3] # post office
G = [0,1,2,3] # school
H = [0,1,2,3] # cafe

countCombinations = 0
Score = []
Parameters = []

for x in itertools.product(AA,BB,A,B,C,D,E,F,G,H):
    
    countVariables = 0

    for item in x:
        countVariables += item
    
    if countVariables == sizeLimit: # valid combination
       # Parameters.append(x)
       # Score.append(distilleBasketTest(x))
        countCombinations += 1

print ("Combinations: " + str(countCombinations))
