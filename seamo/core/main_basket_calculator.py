import pandas as pd
import os
import __init__
import constants as cn
from basket_calculator import BasketCalculator
from coordinate import Coordinate


"""
1. Calculate distances using haversine formula.
2. Filter universe of destinations based on threshold.
    output: haversine_distances.csv
3. Make API calls to Google Distance Matrix to get distances.
    output: api_distances.csv
4. Rank destinations by class and by proximity to a block group.
    output: ranked_destinations.csv
5. Create basket of destinations for each block group.
    output: input_baskets.csv

"""
# Instantiate a basket calculator without an API key.
bc = BasketCalculator('null')
origin_df = BasketCalculator.origin_df
dest_df = BasketCalculator.dest_df
dist_fp = cn.HAVERSINE_DIST_FP
# bc.origins_to_destinations(dist_fp, origin_df, dest_df, 'haversine', True)
api_key = input("Enter your Google API key: ")

bc = BasketCalculator()

distance_df = pd.read_csv(cn.HAVERSINE_DIST_FP) 

cols = [cn.BLOCKGROUP, cn.PAIR, cn.DISTANCE, cn.CLASS,
        cn.GOOGLE_START_LAT, cn.GOOGLE_START_LON,
        cn.GOOGLE_END_LAT, cn.GOOGLE_END_LON]

OUTPUT_FP = cn.API_DIST_FP 
if not os.path.exists(OUTPUT_FP):
    with open(OUTPUT_FP, 'w+') as outf:
        outf.write(','.join(cols))
        outf.write('\n')

with open(OUTPUT_FP, 'a+') as outf:
    # Need to create subset_df
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
   

bc = BasketCalculator('null') 
api_distances = cn.API_DIST_FP
dist_df = pd.read_csv(api_distances)
ranked_df = bc.rank_destinations(dist_df)
ranked_df.to_csv('ranked_destinations.csv')
baskets_df = bc.create_basket(ranked_df, cn.BASKET)
baskets_df.to_csv('input_baskets.csv')
