import init
import cProfile
import os
import sys
import pstats
import trip
import parking_cost as pc
import geocoder as gc
import constants as cn

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

cProfile.run('trip.CarTrip(SEATTLE_ORIGIN, SEATTLE_DESTINATION, DISTANCE, DURATION, BASKET_CATEGORY, PAIR, DEPARTURE_TIME, RANK, DURATION_IN_TRAFFIC)',
	'OUTFILE')
# datadir = os.path.join(cn.TEST_DIR, 'test1000.csv')
# geo = pc.ParkingCost()
# cProfile.run('geo.geocode_csv(datadir)', 'OUTFILE')
# geo = gc.Geocoder()
# cProfile.run('geo.geocode_point(SEATTLE_ORIGIN)', 'OUTFILE')
p = pstats.Stats('OUTFILE')
p.sort_stats('cumtime')
p.print_stats()