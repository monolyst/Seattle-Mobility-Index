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

dist_df = pd.read_csv(cn.HAVERSINE_DIST_FP)

# If the queue does not exist, create it by making a copy of the distance csv
if not os.path.exists(cn.DISTANCE_QUEUE_FP):
    dist_df.to_csv(cn.DISTANCE_QUEUE_FP)

# If the 'stack' file exists, use it
queue_df = pd.read_csv(cn.DISTANCE_QUEUE_FP)  

api_calls = 0
finished_rows = []

with open(OUTPUT_FP, 'a+') as outf:
    for index, row in queue_df.iterrows():
        blockgroup = row[cn.BLOCKGROUP]
        origin_lat = row[cn.GOOGLE_START_LAT]
        origin_lon = row[cn.GOOGLE_START_LON]
        origin = Coordinate(origin_lat, origin_lon)
        end_lat = row[cn.GOOGLE_END_LAT]
        end_lon = row[cn.GOOGLE_END_LON]
        destination = Coordinate(end_lat, end_lon)
        distance = bc.calculate_distance_API(origin, destination)
        # Increment number of API calls made
        api_calls +=1 
        if distance: 
            # If the call was successful, log its index
            finished_rows.append(index)
            dest_class = row[cn.CLASS]
            end_lat = row[cn.GOOGLE_END_LAT]
            end_lon = row[cn.GOOGLE_END_LON]
            pair = row[cn.PAIR] 
            row = [blockgroup, pair, distance, dest_class,
                   origin_lat, origin_lon, end_lat, end_lon]

            outf.write(','.join([str(e) for e in row]))
            outf.write('\n')
        if api_calls == cn.API_CALL_LIMIT:
            break

# Remove rows for which we successfully got data 
queue_df = queue_df.drop(queue_df.index[finished_rows])
queue_df.to_csv(cn.DISTANCE_QUEUE_FP)

api_distances = cn.API_DIST_FP


# For each blockgroup and class of destination, rank by proximity.
dist_df = pd.read_csv(api_distances)
ranked_df = rank_destinations(dist_df)
ranked_df.to_csv(cn.RANKED_DEST_FP)
baskets_df = create_basket(ranked_df, cn.FINAL_BASKET)
baskets_df.to_csv(cn.BASKETS_FP)
# Also need to put out the compressed formats where dests are in one col
bgs = { blockgroup: { cn.ORIGIN : None, cn.DESTINATIONS : [], cn.PAIR: None, cn.CLASS: None } for blockgroup in df[cn.BLOCKGROUP].values }
for index, row in df.iterrows():
    origin = "{0},{1}".format(row[cn.GOOGLE_START_LAT], row[cn.GOOGLE_START_LON])
    destination = "{0},{1}".format(row[cn.GOOGLE_END_LAT], row[cn.GOOGLE_END_LON])
    pair = row[cn.PAIR]

    bgs[row[cn.BLOCKGROUP]][cn.DESTINATIONS].append(destination) 
    bgs[row[cn.BLOCKGROUP]][cn.ORIGIN] = origin
    bgs[row[cn.BLOCKGROUP]][cn.PAIR] = paircols = [cn.BLOCKGROUP, cn.PAIR, cn.ORIGIN, cn.DESTINATIONS]
rows = []
new_df = pd.DataFrame(columns=cols)
for bg, data in bgs.items():
    origin = data[cn.ORIGIN]
    pair = data[cn.PAIR]
    # Separate destinations with a pipe
    dests = "|".join(data[cn.DESTINATIONS])
    new_row = { cn.BLOCKGROUP : bg,
                cn.ORIGIN: origin,
                cn.PAIR: pair,
                cn.DESTINATIONS: dests
                    }
    rows.append(new_row)
new_df = pd.DataFrame(rows, columns=cols)
new_df.to_csv(cn.INPUT_BASKETS_FP)
