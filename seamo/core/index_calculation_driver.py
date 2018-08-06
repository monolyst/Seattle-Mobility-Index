import init
import os
import constants as cn 
from mode_choice_calculator import ModeChoiceCalculator
from affordability_index import AffordabilityIndex
import data_accessor as daq
import pandas as pd

mc = ModeChoiceCalculator()
try:
    daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc.pickle')
except:
    total_trips_df = pd.read_csv(cn.DISTANCES_OUT_FP)
    # Need to drop the duplicates.
    to_drop = total_trips_df[((total_trips_df.destination == "First Hill") | (total_trips_df.destination == "South Lake Union")) & (total_trips_df['class'] == "urban_village")]

    total_trips_df = total_trips_df.drop(to_drop.index)

    # Create a dictionary where keys are blockgroup IDs and values are lists of Trips
    trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df, viable_only=True)
    daq.make_pickle(cn.PICKLE_DIR, trips_per_blockgroup, 'mode_choice_calc.pickle')
else:
    trips_per_blockgroup = daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc.pickle')

# print(trips_per_blockgroup)
ac = AffordabilityIndex(trips_per_blockgroup)
print("checkpoint reached")

# # create cost dataframe for each blockgroup
# # import pdb; pdb.set_trace()
block_cost_df = ac.create_avg_blockgroup_cost_df()
print(block_cost_df.head())

#calculate affordability index scores
# block_cost_index = ac.calculate_score(trips_per_blockgroup)

