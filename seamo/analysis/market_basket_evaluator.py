from datetime import datetime
import init
import constants as cn

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


def vert_hori_ratio(df_destinations, df_blockgroup):

    """
    Calculate the ratio between vertical distance and horizontal distance, for each blockgroup
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    
    df_destinations['vertical_horizontal_ratio_test'] = pd.DataFrame(np.abs( (df_destinations['dest_lat'] - df_destinations['orig_lat']) /
                                                                             (df_destinations['dest_lon'] - df_destinations['orig_lon']) ))
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['vertical_horizontal_ratio_test'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    
    return(result_merged)


def average_distance(df_destinations, df_blockgroup):

    """
    Calculate average travel distance of each blockgroup 
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['distance'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    result_merged.rename(columns = {'distance': 'average_distance_test'}, inplace=True)
    
    return(result_merged)



def distance_from_citycenter(df_destinations, df_blockgroup):

    """
    Calculate Euclidean distance of destination from the city center  
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
   
    df_destinations['distance_from_citycenter_val'] = pd.DataFrame(np.sqrt(
                                                ((df_destinations['dest_lat'] - cn.CITY_CENTER[0]) * cn.DEG_INTO_MILES)**2 + 
                                                ((df_destinations['dest_lon'] - cn.CITY_CENTER[1]) * cn.DEG_INTO_MILES)**2
                                                ))
    
    df_blockgroup2 = df_destinations.groupby(['origin'], as_index=False)['distance_from_citycenter_val'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on='origin', right_on='origin')
    result_merged.rename(columns = {'distance_from_citycenter_val': 'distance_from_citycenter_test'}, inplace=True)
      
    return(result_merged)


def prepare_psrc(psrc_raw):

    """
    This code calculates four features and adds them to the original PSRC data. 
    It just needs to be run once, as we are using it without filtering. 
    input:
        PSRC data (even though we call it raw, its column names are changed and latitude and longitudes are added)
    output:
        PSRC data with proximity ratio, vert_hori_ratio, average distance, and distance from city center
    """
    
    psrc_blockgroup = proximity_ratio(psrc_raw)
    with_vert_hori_ratio = vert_hori_ratio(psrc_raw, psrc_blockgroup)
    with_average_distance = average_distance(psrc_raw, with_vert_hori_ratio)
    with_distance_from_citycenter = distance_from_citycenter(psrc_raw, with_average_distance)
    
    result_merged = with_distance_from_citycenter
    result_merged.sort_values(by=['origin'])
    
    return (result_merged)


def calculate_features(google_input, basket_combination):

    """
    This calculates three features using google API data; need to run separately for each basket combination
    It just needs to be run for every basket combination, as we are filtering it every time.  
    input:
        Google API data, backet combination
    output:
        Google API data with proximity ratio, vert_hori_ratio, average distance, and distance from city center
    """
    
    # Filter to match basket parameters based on rank (distance from destination)
    filtered_data = google_input
    for i in range(len(cn.BASKET_CATEGORIES)):
        filtered_data = filtered_data[(filtered_data['class'] != cn.BASKET_CATEGORIES[i]) | (filtered_data['rank'] <= basket_combination[i])]
   
    # FEATURES: PROXIMITY RATIO, VERTICAL/HORIZONTAL TRAVEL DISTANCES, AVERAGE DISTANCE TO DESTINATION
    
    # Creating google results
    with_proximity_ratio = proximity_ratio(filtered_data.copy())
    with_vert_hori_ratio = vert_hori_ratio(filtered_data.copy(), with_proximity_ratio)
    with_average_distance = average_distance(filtered_data.copy(), with_vert_hori_ratio)
    with_distance_from_citycenter = distance_from_citycenter(filtered_data.copy(), with_average_distance)
    
    final_result = with_distance_from_citycenter.sort_values(by = ['origin'])
    
    return (final_result)

BASKET_SIZE = cn.BASKET_SIZE

def calculate_mse(psrc_output, google_input):

    """
    This calculates three features for each basket combination, saves MSE to compare Google API with PSRC
    input:
        PSRC wth features, Google API data without features
    output:
        Basket combinations, MSEs for each basket
    """

    score = []
    combinations = []

    for x in itertools.product(AA,BB,A,B,C,D,E,F,G,H):
        if (sum(x) == BASKET_SIZE):
            combinations.append(x)
            df_google = calculate_features(google_input, list(x))
            googled_psrc = psrc_output.loc[psrc_output['origin'].isin(df_google['origin'])]
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
    
    
    final_combinations = pd.DataFrame(combinations, columns = cn.BASKET_CATEGORIES)
    #print(final_combinations)
    
    best_loc = final_mses['rank_from_average_distance'].idxmin()
    print("Choose the following combination: \n")
    
    print("The index of the best basket is: ", best_loc)
    print(final_combinations.loc[best_loc])
    
    return(final_combinations, final_mses)


# Load PSRC data and pre-process; column names should be determined at a group meeting
psrc_rawdat = pd.read_csv(DATADIR + "PSRC_full_final_july3.csv", dtype={'origin': str, 'destination': str})

psrc_rawdat['distance'] = pd.to_numeric(psrc_rawdat['distance'], errors='coerce')
#psrc_rawdat.head()


# Load Google API data 
input_destinations = pd.read_csv(DATADIR + 'GoogleMatrix_Places_Dist.csv', dtype={'origin': str})
input_destinations.rename(columns = {'lat': 'dest_lat', 'lng': 'dest_lon', 'orig_lng': 'orig_lon'}, inplace=True)


# Load blockgroup data with latitude and longitudes; will be merged with Google API
blockgroup_mapping = pd.read_csv(PROCESSED_DIR + 'SeattleCensusBlockGroups.csv', dtype={'tract_blkgrp': str})

print("blockgroup_mapping is loaded!")


blockgroup_mapping['tract_blkgrp'] = '530330' + blockgroup_mapping['tract_blkgrp']
orig_pts = blockgroup_mapping.centroid.apply(shapely.wkt.loads)
blockgroup_mapping['orig_lon'] = pd.DataFrame([kk.x for kk in orig_pts])
blockgroup_mapping['orig_lat'] = pd.DataFrame([kk.y for kk in orig_pts])
origin_blockgroups = blockgroup_mapping [['tract_blkgrp', 'orig_lat', 'orig_lon']]



# origin_merged will be an input data for 'evaluate_features' function
origin_merged = pd.merge(left=input_destinations, right=origin_blockgroups, how='left', left_on='origin', right_on='tract_blkgrp')
origin_merged = origin_merged[['origin', 'dest_lat', 'orig_lat','dest_lon', 'orig_lon', 'rank', 'distance', 'class']]

print("Google data are ready!")


# One-time computation of psrc: generate three features
df_psrc = prepare_psrc(psrc_rawdat.copy())
#df_psrc.head()

print("PSRC data are ready!")



comb, res = calculate_mse(df_psrc, origin_merged.copy())
#res
print("The following is the head of combinations")
print(comb.head())

print("\n\n")
print("The following is the head of mses")
print(res.head())

print("all done!")


res.to_csv(PROCESSED_DIR + 'mses.csv')
comb.to_csv(PROCESSED_DIR + 'comb.csv')


