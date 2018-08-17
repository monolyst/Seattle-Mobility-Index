import numpy as np
import pandas as pd
import shapely.wkt
from sklearn.metrics import pairwise_distances
from sklearn.metrics import mean_squared_error

import init
import constants as cn
from coordinate import Coordinate

def proximity_ratio(df_destinations):
    """
    Calculate proximity ratio and summarize by blockgroups
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    lower_bound = cn.BASKET_EVAL_PROX_MIN # 2 miles
    upper_bound = cn.BASKET_EVAL_PROX_MAX # 10 miles
    
    # Ratio of trips under 2 miles to trips between 2 and 10 miles
    df_destinations['dist_under_2'] = np.where(df_destinations[cn.DISTANCE] < lower_bound, 1, 0)
    df_destinations['dist_2_to_10'] = np.where((df_destinations[cn.DISTANCE] >= lower_bound) & (df_destinations[cn.DISTANCE] < upper_bound), 1, 0)
    df_blockgroup = df_destinations.groupby([cn.ORIGIN], as_index=False).agg({'dist_under_2':sum,'dist_2_to_10':sum})
    
    # Remove rows with zero denominators
    df_blockgroup = df_blockgroup[df_blockgroup['dist_2_to_10'] != 0]   
    
    # Make new column with the data
    df_blockgroup[cn.PROX_RATIO] = df_blockgroup['dist_under_2'] / df_blockgroup['dist_2_to_10']

    return df_blockgroup[[cn.ORIGIN, cn.PROX_RATIO]]


def vert_hori_ratio(df_destinations, df_blockgroup):
    """
    Calculate the ratio between vertical distance and horizontal distance, for each blockgroup
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    df_destinations[cn.VERT_HORI_RATIO] = pd.DataFrame(np.abs( (df_destinations['dest_lat'] - df_destinations['orig_lat']) /
                                                                             (df_destinations['dest_lon'] - df_destinations['orig_lon']) ))
    df_blockgroup2 = df_destinations.groupby([cn.ORIGIN], as_index=False)[cn.VERT_HORI_RATIO].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on=cn.ORIGIN, right_on=cn.ORIGIN)
    
    return result_merged


def average_distance(df_destinations, df_blockgroup):
    """
    Calculate average travel distance of each blockgroup 
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    df_blockgroup2 = df_destinations.groupby([cn.ORIGIN], as_index=False)[cn.DISTANCE].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on=cn.ORIGIN, right_on=cn.ORIGIN)
    result_merged.rename(columns = {cn.DISTANCE: cn.AVG_DIST}, inplace=True)
    
    return result_merged

def dist_from_cc(df):
    """
    Helper function to create a new column in a DataFrame with dist to city center
    """
    coordinate = Coordinate(df['dest_lat'], df['dest_lon'])
    city_center = Coordinate(cn.CITY_CENTER[0], cn.CITY_CENTER[1])
    return city_center.haversine_distance(coordinate) 

def distance_from_citycenter(df_destinations, df_blockgroup):
    """
    Calculate Euclidean distance of destination from the city center  
    input: 
        df_destination - data frame with distance, trip-level data
    output:
        df_blockgroup - data frame with origin blockgroup and proximity ratio
    """
    
    df_destinations['distance_from_citycenter_val'] = df_destinations.apply(dist_from_cc, axis=1) 
    
    df_blockgroup2 = df_destinations.groupby([cn.ORIGIN], as_index=False)['distance_from_citycenter_val'].mean()
    result_merged = pd.merge(left=df_blockgroup, right=df_blockgroup2, how='inner', left_on=cn.ORIGIN, right_on=cn.ORIGIN)
    result_merged.rename(columns = {'distance_from_citycenter_val': 'distance_from_citycenter_test'}, inplace=True)
      
    return result_merged


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
    result_merged.sort_values(by=[cn.ORIGIN])
    
    return result_merged


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
    
    final_result = with_distance_from_citycenter.sort_values(by = [cn.ORIGIN])
    
    return final_result


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

    for x in cn.BASKET_COMBOS:
        if (sum(x) == cn.BASKET_SIZE):
            combinations.append(x)
            df_google = calculate_features(google_input, list(x))
            googled_psrc = psrc_output.loc[psrc_output[cn.ORIGIN].isin(df_google[cn.ORIGIN])]
            proximity_ratio_mse = mean_squared_error(df_google[cn.PROX_RATIO], googled_psrc[cn.PROX_RATIO])
            vert_hori_ratio_mse = mean_squared_error(df_google[cn.VERT_HORI_RATIO], googled_psrc[cn.VERT_HORI_RATIO])
            average_distance_mse = mean_squared_error(df_google[cn.AVG_DIST], googled_psrc[cn.AVG_DIST])
            distance_from_citycenter_mse = mean_squared_error(df_google['distance_from_citycenter_test'], googled_psrc['distance_from_citycenter_test'])

            mses = (proximity_ratio_mse, vert_hori_ratio_mse, average_distance_mse, distance_from_citycenter_mse)
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
    
    best_loc = final_mses['rank_from_average_distance'].idxmin()
    print("Choose the following combination: \n")
    
    print("The index of the best basket is: ", best_loc)
    print(final_combinations.loc[best_loc])
    
    return final_combinations, final_mses


# Load PSRC data and pre-process
psrc_rawdat = pd.read_csv(cn.PSRC_FP, dtype={cn.ORIGIN: str, cn.DESTINATION: str})

psrc_rawdat[cn.DISTANCE] = pd.to_numeric(psrc_rawdat[cn.DISTANCE], errors='coerce')


# Load Google API data 
input_destinations = pd.read_csv(cn.RAW_DIR + 'GoogleMatrix_Places_Dist.csv', dtype={cn.ORIGIN: str})
input_destinations.rename(columns = {'lat': 'dest_lat', 'lng': 'dest_lon', 'orig_lng': 'orig_lon'}, inplace=True)

# Load blockgroup data with latitude and longitudes; will be merged with Google API
blockgroup_mapping = pd.read_csv(cn.PROCESSED_DIR + 'SeattleCensusBlockGroups.csv', dtype={'tract_blkgrp': str})

print("blockgroup_mapping is loaded!")


blockgroup_mapping['tract_blkgrp'] = '530330' + blockgroup_mapping['tract_blkgrp']
orig_pts = blockgroup_mapping.centroid.apply(shapely.wkt.loads)
blockgroup_mapping['orig_lon'] = pd.DataFrame([kk.x for kk in orig_pts])
blockgroup_mapping['orig_lat'] = pd.DataFrame([kk.y for kk in orig_pts])
origin_blockgroups = blockgroup_mapping [['tract_blkgrp', 'orig_lat', 'orig_lon']]

# origin_merged will be an input data for 'evaluate_features' function
origin_merged = pd.merge(left=input_destinations, right=origin_blockgroups, how='left', left_on=cn.ORIGIN, right_on='tract_blkgrp')
origin_merged = origin_merged[[cn.ORIGIN, 'dest_lat', 'orig_lat','dest_lon', 'orig_lon', 'rank', cn.DISTANCE, 'class']]

print("Google data are ready!")

# One-time computation of psrc: generate three features
df_psrc = prepare_psrc(psrc_rawdat.copy())

print("PSRC data are ready!")

comb, res = calculate_mse(df_psrc, origin_merged.copy())
print("The following is the head of combinations")
print(comb.head())

print("\n\n")
print("The following is the head of mses")
print(res.head())

print("all done!")

comb.to_csv(cn.BASKET_COMBO_FP)
res.to_csv(cn.MSES_FP)
