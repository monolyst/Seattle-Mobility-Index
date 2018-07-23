from datetime import datetime
import init
import constants 

import itertools
import json
import math
import os
import time
import string

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import shapely.wkt
from sklearn.metrics import pairwise_distances
from sklearn.metrics import mean_squared_error
try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2


"""
TEST_ORIGIN = '530330001003'
BASKET_CATEGORIES = ["urban village", "citywide", "destination park", "supermarket", "library", 
              "hospital", "pharmacy", "post_office", "school", "cafe"]
BASKET_SIZE = 25

DEG_INTO_MILES = 69
CITY_CENTER = [47.6062, -122.3321]
"""
# Parameter domains
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


FILEPATH = os.path.join(os.pardir, os.pardir, 'seamo/analysis/')
DATADIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/')
PROCESSED_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/')


def proximity_ratio(df_destinations):
    
    """
    Calculate proximity ratio and summarize by blockgroups
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    # proximity ratio = no. trips under 2 miles / no. trips between 2 and 10 miles; rows with zero denominators are removed
    df_destinations['dist_under_2'] = np.where(df_destinations['distance'] < 2.0, 1, 0)
    df_destinations['dist_2_to_10'] = np.where((df_destinations['distance'] >= 2.0) & (df_destinations['distance'] < 10.0), 1, 0)
    df_blockgroup = df_destinations.groupby(['origin'], as_index=False).agg({'dist_under_2':sum,'dist_2_to_10':sum})
    
    df_blockgroup = df_blockgroup[df_blockgroup['dist_2_to_10'] != 0]   
    df_blockgroup['proximity_ratio_test'] = df_blockgroup['dist_under_2'] / df_blockgroup['dist_2_to_10']
    """
    print((df_destinations.loc[df_destinations['origin'] == '530330048003']))
    print((df_destinations.loc[df_destinations['origin'] == '530330049002']))
    print((df_destinations.loc[df_destinations['origin'] == '530330049003']))    
    """
    return(df_blockgroup[['origin', 'proximity_ratio_test']])
    #return(df_blockgroup[['origin', 'proximity_ratio_test', 'dist_under_2', 'dist_2_to_10']])


def vert_hori_ratio(df_destinations, df_blockgroup):
    
    df_destinations['vertical_horizontal_ratio_test'] = pd.DataFrame(np.abs( (df_destinations['dest_lat'] - df_destinations['orig_lat']) / (df_destinations['dest_lon'] - df_destinations['orig_lon']) ))
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['vertical_horizontal_ratio_test'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    
    return(result_merged)


def average_distance(df_destinations, df_blockgroup):
    
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['distance'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    result_merged.rename(columns = {'distance': 'average_distance_test'}, inplace=True)
    
    return(result_merged)



def distance_from_citycenter(df_destinations, df_blockgroup):
   
    df_destinations['distance_from_citycenter_val'] = pd.DataFrame(np.sqrt(
                                                ((df_destinations['dest_lat'] - CITY_CENTER[0]) * DEG_INTO_MILES)**2 + 
                                                ((df_destinations['dest_lon'] - CITY_CENTER[1]) * DEG_INTO_MILES)**2
                                                ))
    
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['distance_from_citycenter_val'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    result_merged.rename(columns = {'distance_from_citycenter_val': 'distance_from_citycenter_test'}, inplace=True)
      
    return(result_merged)


def prepare_psrc(psrc_raw):
        
    # This will compute three features using PSRC data; just need to run it once
    psrc_blockgroup = proximity_ratio(psrc_raw)
    with_vert_hori_ratio = vert_hori_ratio(psrc_raw, psrc_blockgroup)
    with_average_distance = average_distance(psrc_raw, with_vert_hori_ratio)
    with_distance_from_citycenter = distance_from_citycenter(psrc_raw, with_average_distance)
    
    """
    # calculate weighted proximity ratio
    psrc_raw['dist_under_2'] = np.where(psrc_raw['distance'] < 2.0, 1, 0)
    psrc_raw['dist_2_to_10'] = np.where((psrc_raw['distance'] >= 2.0) & (psrc_raw['distance'] < 10.0), 1, 0)     
    psrc_raw['weighted_under_2'] = psrc_raw['weight'] * psrc_raw['dist_under_2']
    psrc_raw['weighted_2_to_10'] = psrc_raw['weight'] * psrc_raw['dist_2_to_10']    
    df_blockgroup2 = psrc_raw.groupby(['origin'], as_index=False).agg({'weighted_under_2':sum,'weighted_2_to_10':sum})
    df_blockgroup2['weighted_proximity_ratio'] = df_blockgroup2['weighted_under_2'] / df_blockgroup2['weighted_2_to_10']
    
    result_merged = pd.merge(left=with_distance_from_citycenter, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    result_merged.dropna(inplace=True)
    """
    result_merged = with_distance_from_citycenter
    result_merged.sort_values(by=['origin'])
    
    return (result_merged)


def calculate_features(google_input, basket_combination):
    
    # This calculates three features using google API data; need to run separately for each basket combination
    
    # Filter to match basket parameters based on rank (distance from destination)
    filtered_data = google_input
    for i in range(len(BASKET_CATEGORIES)):
        filtered_data = filtered_data[(filtered_data['class'] != BASKET_CATEGORIES[i]) | (filtered_data['rank'] <= basket_combination[i])]
   
    # FEATURES: PROXIMITY RATIO, VERTICAL/HORIZONTAL TRAVEL DISTANCES, AVERAGE DISTANCE TO DESTINATION
    
    # Creating google results
    with_proximity_ratio = proximity_ratio(filtered_data.copy())
    with_vert_hori_ratio = vert_hori_ratio(filtered_data.copy(), with_proximity_ratio)
    with_average_distance = average_distance(filtered_data.copy(), with_vert_hori_ratio)
    with_distance_from_citycenter = distance_from_citycenter(filtered_data.copy(), with_average_distance)
    
    final_result = with_distance_from_citycenter.sort_values(by = ['origin'])
    
    return (final_result)


def calculate_mse(psrc_output, google_input):

    score = []
    combinations = []

    for x in itertools.product(AA,BB,A,B,C,D,E,F,G,H):
        if (sum(x) == BASKET_SIZE):
            combinations.append(x)
            df_google = calculate_features(google_input, list(x))
            #df_google_result = df_google.sort_values(by=['origin'])
            googled_psrc = psrc_output.loc[psrc_output['origin'].isin(df_google['origin'])]
            #df_psrc_result = googled_psrc.sort_values(by=['origin'])
            proximity_ratio_mse = mean_squared_error(df_google['proximity_ratio_test'], googled_psrc['proximity_ratio_test'])
            vert_hori_ratio_mse = mean_squared_error(df_google['vertical_horizontal_ratio_test'], googled_psrc['vertical_horizontal_ratio_test'])
            average_distance_mse = mean_squared_error(df_google['average_distance_test'], googled_psrc['average_distance_test'])
            distance_from_citycenter_mse = mean_squared_error(df_google['distance_from_citycenter_test'], googled_psrc['distance_from_citycenter_test'])

            mses = (proximity_ratio_mse, vert_hori_ratio_mse, average_distance_mse, distance_from_citycenter_mse)
            #print("combination is :", x)
            score.append(mses)
            if (len(combinations) % 5000 == 0):
                print("Still Processing..")
                print("Idx+1 of combination is: ", len(combinations))

    print("Total number of combinations: " + str(len(combinations)))
    print()
    
    final_mses = pd.DataFrame(score, columns = ['from_proximity_ratio', 'from_vert_hori_ratio', 'from_average_distance', 'from_distance_citycenter'])
    final_mses['rank_from_proximity_ratio'] = final_mses['from_proximity_ratio'].rank(ascending=1)
    final_mses['rank_from_vert_hori_ratio'] = final_mses['from_vert_hori_ratio'].rank(ascending=1)
    final_mses['rank_from_average_distance'] = final_mses['from_average_distance'].rank(ascending=1)    
    final_mses['rank_from_distance_citycenter'] = final_mses['from_distance_citycenter'].rank(ascending=1)    
    
    
    final_combinations = pd.DataFrame(combinations, columns = BASKET_CATEGORIES)
    #print(final_combinations)
    
    best_loc = final_mses['rank_from_average_distance'].idxmin()
    print("Choose the following combination: \n")
    
    print("The index of the best basket is: ", best_loc)
    print(final_combinations.loc[best_loc])
    
    return(final_combinations, final_mses)



    #fp = FILEPATH + str(input_file) + '.csv'
    #df = pd.read_csv(fp)

# Load PSRC data and pre-process; column names should be determined at a group meeting
psrc_rawdat = pd.read_csv(DATADIR + "PSRC_full_final_july3.csv", dtype={'origin': str, 'destination': str})
"""
psrc_rawdat['origin'] = '530330' + psrc_rawdat['o_bg']
psrc_rawdat['destination'] = '530330' + psrc_rawdat['d_bg']
psrc_orig_pts = psrc_rawdat['o_bg_lat_long'].apply(shapely.wkt.loads)
psrc_dest_pts = psrc_rawdat['d_bg_lat_long'].apply(shapely.wkt.loads)
psrc_rawdat['orig_lng'] = pd.DataFrame([kk.x for kk in psrc_orig_pts])
psrc_rawdat['orig_lat'] = pd.DataFrame([kk.y for kk in psrc_orig_pts])
psrc_rawdat['dest_lng'] = pd.DataFrame([kk.x for kk in psrc_dest_pts])
psrc_rawdat['dest_lat'] = pd.DataFrame([kk.y for kk in psrc_dest_pts])
psrc_rawdat.drop(columns = ['o_bg', 'o_bg_lat_long', 'd_bg', 'd_bg_lat_long'], inplace=True)
psrc_rawdat.rename(columns = {'trip_path_distance': 'distance', 'trip_weight_revised': 'weight'}, inplace=True)
"""

"""

psrc_rawdat['distance'] = pd.to_numeric(psrc_rawdat['distance'], errors='coerce')
psrc_rawdat.head()


# Load Google API data 
# df_sample = pd.read_csv('Proximity_Ratio.csv', dtype={'bg_origin': str}) 
input_destinations = pd.read_csv('GoogleMatrix_Places_Dist.csv', dtype={'origin': str})
input_destinations.rename(columns = {'lat': 'dest_lat', 'lng': 'dest_lon', 'orig_lng': 'orig_lon'}, inplace=True)

# Load blockgroup data with latitude and longitudes; will be merged with Google API
blockgroup_mapping = pd.read_csv('SeattleCensusBlockGroups.csv', dtype={'tract_blkgrp': str})
blockgroup_mapping['tract_blkgrp'] = '530330' + blockgroup_mapping['tract_blkgrp']
orig_pts = blockgroup_mapping.centroid.apply(shapely.wkt.loads)
blockgroup_mapping['orig_lon'] = pd.DataFrame([kk.x for kk in orig_pts])
blockgroup_mapping['orig_lat'] = pd.DataFrame([kk.y for kk in orig_pts])
origin_blockgroups = blockgroup_mapping [['tract_blkgrp', 'orig_lat', 'orig_lon']]


# origin_merged will be an input data for 'evaluate_features' function
origin_merged = pd.merge(left=input_destinations, right=origin_blockgroups, how='left', left_on='origin', right_on='tract_blkgrp')
origin_merged = origin_merged[['origin', 'dest_lat', 'orig_lat','dest_lon', 'orig_lon', 'rank', 'distance', 'class']]

# One-time computation of psrc: generate three features
df_psrc = prepare_psrc(psrc_rawdat.copy())
df_psrc.head()


comb, res = calculate_mse(df_psrc, origin_merged.copy())
#res
comb.head()
res.head()

res.to_csv('Result/mses.csv')
comb.to_csv('Result/comb.csv')



"""
