"""
Usage: (from seamo/) python core/persona_avail.py

This script creates a ModeChoiceCalculator for each Persona and produces
mode viability scores for each blockgroup for each Persona based on their 
unique thresholds.

These scores are saved in individual CSV files in the seamo/data/processed/csv_files
folder.
"""
import init
import os
import constants as cn 
from trip import Trip
from mode_choice_calculator import ModeChoiceCalculator
from affordability_index import AffordabilityIndex
import data_accessor as daq
import time

import os
import pandas as pd

PERSONA_DICTS = pd.read_csv(cn.PERSONA_FP, index_col=0).to_dict('index')

total_trips_df = pd.read_csv(cn.WEEKDAY_DISTANCES_OUT_FP)
# Need to drop the duplicates.
# First Hill and SLU are only 'citywide' destinations in the baskets,
# never 'urban_village'
to_drop = total_trips_df[((total_trips_df.destination == "First Hill") |
                          (total_trips_df.destination == "South Lake Union"))
                          & (total_trips_df['class'] == "urban_village")]

total_trips_df = total_trips_df.drop(to_drop.index)

for persona, attrs in PERSONA_DICTS.items():
    driving_threshold = attrs[cn.DRIVE_THRESHOLD]
    transit_threshold = attrs[cn.TRANSIT_THRESHOLD] 
    biking_threshold = attrs[cn.BIKE_THRESHOLD]
    walking_threshold = attrs[cn.WALK_THRESHOLD]
    mc = ModeChoiceCalculator(driving_threshold,
                              biking_threshold,
                              transit_threshold,
                              walking_threshold)
    trips = mc.trips_per_blockgroup(total_trips_df)
    avail_df = mc.create_availability_df(trips) 
    avail_df.to_csv(os.path.join(cn.CSV_DIR, 'wkday_mode_avail_{0}.csv'.format(persona)))
