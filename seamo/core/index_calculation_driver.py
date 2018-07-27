import init
import os
import constants as cn 
from trip import Trip
from mode_choice_calculator import ModeChoiceCalculator

import pandas as pd

mc = ModeChoiceCalculator()

total_trips_df = pd.read_csv(cn.DISTANCES_OUT_FP)

# Create a dictionary where keys are blockgroup IDs and values are lists of Trips
trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df)
