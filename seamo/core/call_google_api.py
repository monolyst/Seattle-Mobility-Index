import pandas as pd
import os
import __init__
import constants as cn
from basket_destination_calculator import BasketCalculator
from coordinate import Coordinate


if __name__ == "__main__":
    
    """
    Ask the user for their API key.
    
    Calculate distances using haversine and filter.

    Then, using the filtered distances, call Google (only some)
    """
    api_key = input("Enter your Google API key: ")

    # Super hacky way to decide which part of the file to use.
    day_of_week = input("What day is it? ")
    
    bc = BasketCalculator(api_key)

    distance_df = pd.read_csv(cn.HAVERSINE_DIST_FP) 

    if day_of_week == "Friday":
        # subset_df = distance_df.iloc[:80000]
        # subset_df = distance_df.iloc[51165:80000]
        pass
    elif day_of_week == "Saturday":
        # subset_df = distance_df.iloc[80000:180000]
        subset_df = distance_df.iloc[55785:155785]
    elif day_of_week == "Sunday":
        # subset_df = distance_df.iloc[165707:255785]
        # subset_df = distance_df.iloc[180000:280000]
        subset_df = distance_df.iloc[188342:300000]
    else:
        subset_df = distance_df[300001:]

    cols = [cn.BLOCKGROUP, cn.PAIR, cn.DISTANCE, cn.CLASS,
            cn.GOOGLE_START_LAT, cn.GOOGLE_START_LON,
            cn.GOOGLE_END_LAT, cn.GOOGLE_END_LON]
        

    OUTPUT_FP = cn.API_DIST_FP 
    if not os.path.exists(OUTPUT_FP):
        with open(OUTPUT_FP, 'w+') as outf:
            outf.write(','.join(cols))
            outf.write('\n')

    with open(OUTPUT_FP, 'a+') as outf:
        for index, row in subset_df.iterrows():
            blockgroup = row[cn.BLOCKGROUP]
            origin_lat = row[cn.GOOGLE_START_LAT]
            origin_lon = row[cn.GOOGLE_START_LON]
            origin = Coordinate(origin_lat, origin_lon)
            end_lat = row[cn.GOOGLE_END_LAT]
            end_lon = row[cn.GOOGLE_END_LON]
            destination = Coordinate(end_lat, end_lon)
            distance = bc.calculate_distance_API(origin, destination)
            if distance: 
                dest_class = row[cn.CLASS]
                end_lat = row[cn.GOOGLE_END_LAT]
                end_lon = row[cn.GOOGLE_END_LON]
                pair = row[cn.PAIR] 
                row = [blockgroup, pair, distance, dest_class,
                       origin_lat, origin_lon, end_lat, end_lon]

                outf.write(','.join([str(e) for e in row]))
                outf.write('\n')
       

