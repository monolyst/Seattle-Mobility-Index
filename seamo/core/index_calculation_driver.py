import init
import os
import constants as cn 
from mode_choice_calculator import ModeChoiceCalculator
from affordability_index import AffordabilityIndex
import data_accessor as daq
import pandas as pd
import time

mc = ModeChoiceCalculator()
# try:
#     daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc.pickle')
# except:
# total_trips_df = pd.read_csv(cn.WEEKDAY_DISTANCES_OUT_FP,
#     dtype={cn.BLOCK_GROUP: str, cn.DEST_BLOCK_GROUP: str})
# trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df, viable_only=True)
#     daq.make_pickle(cn.PICKLE_DIR, trips_per_blockgroup, 'mode_choice_calc.pickle')
# # else:
trips_per_blockgroup = daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc.pickle')


ac = AffordabilityIndex(trips_per_blockgroup)
# print("checkpoint reached")
# start = time.time()
# try:
#     daq.open_pickle(cn.PICKLE_DIR, 'afford_costs.pickle')
# except:
#     block_cost_df = ac.create_avg_blockgroup_cost_df()
#     daq.make_pickle(cn.PICKLE_DIR, block_cost_df, 'afford_costs.pickle')
# else:
#     block_cost_df = daq.open_pickle(cn.PICKLE_DIR, 'afford_costs.pickle')

# end = time.time()


# # print(block_cost_df.head())
# print(end-start, 'seconds')

#calculate affordability index scores
block_cost_index = ac.calculate_score()
a_scores = block_cost_index.loc[:, (cn.KEY, cn.COST, cn.RELATIVE_COST, cn.SCALED, cn.RELATIVE_SCALED,
    cn.AVG_DURATION, cn.FASTEST, cn.DIRECT_COST, cn.CHEAPEST)]
print(a_scores.sort_values(by=cn.RELATIVE_COST).head())
# daq.write_to_csv(a_scores, 'sample_affordability_with_rel.csv')

