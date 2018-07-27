import init
import os
import constants as cn 
from trip import Trip
from mode_choice_calculator import ModeChoiceCalculator
from affordability_index import AffordabilityIndex

import os
import pandas as pd

mc = ModeChoiceCalculator()
ac = AffordabilityIndex()

total_trips_df = pd.read_csv(cn.DISTANCES_OUT_FP)

# Create a dictionary where keys are blockgroup IDs and values are lists of Trips
trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df)


#create cost dataframe for each blockgroup
# import pdb; pdb.set_trace()
#block_cost_df = ac.create_blockgroup_cost_df(trips_per_blockgroup)

#calculate affordability index score
block_cost_index = ac.calculate_score(trips_per_blockgroup)