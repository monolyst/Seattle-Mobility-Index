import pandas as pd
import os
import __init__
import constants as cn
from basket_calculator import * 
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
origin_df = pd.read_csv(cn.ORIGIN_FP) 
dest_df = pd.read_csv(cn.DEST_FP) 

# Calculate distances between origins and destinations using haversine forumla
# Pre-filter the universe of destinations using a proximity threshold
dist_df = origins_to_destinations(origin_df, dest_df, 'haversine', True)
dist_df.to_csv(cn.HAVERSINE_DIST_FP)



# Call Google Distance Matrix API
api_key = input("Enter your Google API key: ")

cols = [cn.BLOCKGROUP, cn.PAIR, cn.DISTANCE, cn.CLASS,
        cn.GOOGLE_START_LAT, cn.GOOGLE_START_LON,
        cn.GOOGLE_END_LAT, cn.GOOGLE_END_LON]

OUTPUT_FP = cn.API_DIST_FP 
if not os.path.exists(OUTPUT_FP):
    with open(OUTPUT_FP, 'w+') as outf:
        outf.write(','.join(cols))
        outf.write('\n')

# Need to look at index of last row
# count lines that are in cn.API_DIST_FP
# count lines that are in error_log

# How to keep ones "on the stack" that didn't work?
subset_df = dist_df[index:] 

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
   
api_distances = cn.API_DIST_FP
dist_df = pd.read_csv(api_distances)
ranked_df = rank_destinations(dist_df)
ranked_df.to_csv('ranked_destinations.csv')
baskets_df = create_basket(ranked_df, cn.BASKET)
baskets_df.to_csv('baskets.csv')
# Also need to put out the compressed formats where dests are in one col
bgs = { blockgroup: { 'origin' : None, 'destinations' : [], 'pair': None, 'class': None } for blockgroup in df['BLOCKGROUP'].values }
for index, row in df.iterrows():
    origin = "{0},{1}".format(row['start_lat'], row['start_lon'])
    destination = "{0},{1}".format(row['end_lat'], row['end_lon'])
    pair = row['pair']

    
    
    bgs[row['BLOCKGROUP']]['destinations'].append(destination) 
    bgs[row['BLOCKGROUP']]['origin'] = origin
    bgs[row['BLOCKGROUP']]['pair'] = paircols = ['BLOCKGROUP', 'pair', 'origin', 'destinations']
rows = []
new_df = pd.DataFrame(columns=cols)
for bg, data in bgs.items():
    origin = data['origin']
    pair = data['pair']
    dests = " | ".join(data['destinations'])
    new_row = { 'BLOCKGROUP' : bg,
                'origin': origin,
                'pair': pair,
                'destinations': dests
                    }
    rows.append(new_row)
new_df = pd.DataFrame(rows, columns=cols)
new_df.to_csv('input_baskets.csv')
