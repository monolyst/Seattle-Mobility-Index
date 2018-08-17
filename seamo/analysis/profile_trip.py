import init
import cProfile
import os
import sys
import pstats
from trip import CarTrip
import parking_cost as pc
import geocoder as gc
import constants as cn
import geocoder_driver as gd
from affordability_index import AffordabilityIndex
import data_accessor as daq

SEATTLE_ORIGIN = (47.6145, -122.3210)
SEATTLE_DESTINATION = (47.6145, -122.3210)

NONSEATTLE_ORIGIN = (-122.3210, 47.6145)
NONSEATTLE_DESTINATION = (-122.3210, 47.6145)

DURATION = 32.183333
DISTANCE = 16.040398
DURATION_IN_TRAFFIC = 3.303167
BASKET_CATEGORY = cn.CITYWIDE
PAIR = '530330006001-Overlake-Redmond'
DEPARTURE_TIME = '2018-06-06 12:41:31.092964'
RANK = 14.0
BASE_COST = DURATION * cn.VOT_RATE / cn.MIN_TO_HR
PARKING_COST = 3.0

# cProfile.run('trip.CarTrip(SEATTLE_ORIGIN, SEATTLE_DESTINATION, DISTANCE, DURATION, BASKET_CATEGORY, PAIR, DEPARTURE_TIME, RANK, DURATION_IN_TRAFFIC)',
	# 'OUTFILE')

origin = '530330094004'
origin2 = '530330094004'
dest_lat = 47.6145
dest_lon = -122.3210
duration = 32.183333
distance = 16.040398
duration_in_traffic = 3.303167
basket_category = 'citywide'
departure_time = '2018-06-06 12:41:31.092964'


def test_trip():
    car = CarTrip(origin, dest_lat, dest_lon, distance, duration, basket_category, departure_time, duration_in_traffic)
    car.set_cost()
    cost = car.cost

trips_per_blockgroup = daq.open_pickle(cn.PICKLE_DIR, 'mode_choice_calc.pickle')
def test_a_index():
    a_index = AffordabilityIndex(trips_per_blockgroup)
    cost = a_index.create_avg_blockgroup_cost_df()

cProfile.run('test_a_index()', 'OUTFILE')

# datadir = os.path.join(cn.TEST_DIR, 'test1000.csv')
# geo = pc.ParkingCost()
# cProfile.run('geo.geocode_csv(datadir)', 'OUTFILE')
# geo = gc.Geocoder()
# cProfile.run('geo.geocode_point(SEATTLE_ORIGIN)', 'OUTFILE')
p = pstats.Stats('OUTFILE')
p.sort_stats('cumtime')
p.print_stats()