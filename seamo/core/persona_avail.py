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


PERSONA_DICTS = pd.read_csv(cn.SAMPLE_PERSONA_FP, index_col=0).to_dict('index')

total_trips_df = pd.read_csv(os.path.join(cn.CSV_DIR, 'google_dist_matrix_out.csv'))
# Need to drop the duplicates.
# First Hill and SLU are only 'citywide' destinations in the baskets,
# never 'urban_village'
to_drop = total_trips_df[((total_trips_df.destination == "First Hill") |
                          (total_trips_df.destination == "South Lake Union"))
                          & (total_trips_df['class'] == "urban_village")]

total_trips_df = total_trips_df.drop(to_drop.index)

p0 = PERSONA_DICTS['family-(wo)man'] 
p1 = PERSONA_DICTS['fit-urbanites'] 
p2 = PERSONA_DICTS['tired-commuter'] 
p3 = PERSONA_DICTS['jolly-retiree']
p4 = PERSONA_DICTS['olde-Seattleite']

for persona, attrs in PERSONA_DICTS.items():
    driving_threshold = attrs['driving_threshold']
    transit_threshold = attrs['transit_threshold'] 
    biking_threshold = attrs['biking_threshold']
    walking_threshold = attrs['walking_threshold']
    mc = ModeChoiceCalculator(driving_threshold,
                              transit_threshold,
                              biking_threshold,
                              walking_threshold)
    trips = mc.trips_per_blockgroup(total_trips_df)
    avail_df = mc.create_availability_df(trips) 
    avail_df.to_csv('mode_availability_{0}.csv'.format(persona))
