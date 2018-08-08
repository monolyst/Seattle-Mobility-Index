import init
import os
import constants as cn 
from mode_choice_calculator import ModeChoiceCalculator
from affordability_index import AffordabilityIndex
import data_accessor as daq
import pandas as pd
import time

mc = ModeChoiceCalculator()
try:
    daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc10000.pickle')
except:
    total_trips_df = pd.read_csv(cn.WEEKDAY_DISTANCES_OUT_FP,
        dtype={cn.BLOCK_GROUP: str, cn.DEST_BLOCK_GROUP: str}).head(10000)
    # Need to drop the duplicates.
    # to_drop = total_trips_df[((total_trips_df.destination == "First Hill") | (total_trips_df.destination == "South Lake Union")) & (total_trips_df['class'] == "urban_village")]

    # total_trips_df = total_trips_df.drop(to_drop.index)

    # Create a dictionary where keys are blockgroup IDs and values are lists of Trips
    # import pdb; pdb.set_trace()
    trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df, viable_only=True)
    daq.make_pickle(cn.PICKLE_DIR, trips_per_blockgroup, 'mode_choice_calc10000.pickle')
else:
    trips_per_blockgroup = daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc10000.pickle')


ac = AffordabilityIndex(trips_per_blockgroup)
print("checkpoint reached")
start = time.time()
try:
    daq.open_pickle(cn.PICKLE_DIR, 'afford_costs10000.pickle')
except:
    block_cost_df = ac.create_avg_blockgroup_cost_df()
    daq.make_pickle(cn.PICKLE_DIR, block_cost_df, 'afford_costs10000.pickle')
else:
    block_cost_df = daq.open_pickle(cn.PICKLE_DIR, 'afford_costs10000.pickle')

end = time.time()


print(block_cost_df.head())
print(end-start, 'seconds')

#calculate affordability index scores
# block_cost_index = ac.calculate_score(trips_per_blockgroup)

