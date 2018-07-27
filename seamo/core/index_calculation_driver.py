import init
import constants as cn 
from trip import Trip
from mode_choice_calculator import ModeChoiceCalculator

import os
import pandas as pd

mc = ModeChoiceCalculator()

driving_df = pd.read_csv(os.path.join(cn.CSV_DIR, 'google_dist_matrix_out_driving.csv'))
biking_df = pd.read_csv(os.path.join(cn.CSV_DIR, 'google_dist_matrix_out_biking.csv'))
walking_df = pd.read_csv(os.path.join(cn.CSV_DIR, 'google_dist_matrix_out_walking.csv'))
transit_df = pd.read_csv(os.path.join(cn.CSV_DIR, 'google_dist_matrix_out_transit.csv'))

# Concatenate all the trip data
total_trips_df = pd.concat([driving_df,walking_df,transit_df,biking_df])

# Create a dictionary where keys are blockgroup IDs and values are lists of Trips
trips_per_blockgroup = mc.trips_per_blockgroup(total_trips_df)
