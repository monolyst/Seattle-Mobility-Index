# import pdb; pdb.set_trace()
import init
import os
import core.geocoder as geocoder
import core.parking_cost as parking_cost
import preproc.geography_processor as gp
import constants as cn
import time
from dateutil import parser
import datetime as dt
import trip


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

geo = geocoder.Geocoder()
# (47.51008433, -122.3805399)
# decoded = geo.get_blockgroup((47.6145, -122.3210)).item()
# decoded = geo.get_blockgroup((47.6145, -122.3210))
decoded = geo.geocode_point((47.615523, -122.199049))
decoded1 = geo.geocode_point((47.6145, -122.3210))
print(decoded)
print(decoded1)
#print(decoded.columns)
# print(decoded)
# print(geo.dataframe)
# print(geo.dataframe

# start = time.time()
# def run_code():
#     for repititions in range(100):
#         trip.CarTrip(SEATTLE_ORIGIN, SEATTLE_DESTINATION, DISTANCE, DURATION, BASKET_CATEGORY, PAIR, DEPARTURE_TIME, RANK, DURATION_IN_TRAFFIC)
        # pc = parking_cost.ParkingCost()
        # # decoded = pc.geocode_csv(os.path.join(cn.TEST_DIR, 'test1000.csv'))
        # decoded = pc.geocode_point((47.6145, -122.3210))
# end = time.time()
# decoded1 = pc.geocode_point((-122.3210, 47.6145))
# print(decoded)
# elapsed = parser.parse(end-start)
# print(end-start, 'seconds')
# print(pc.dataframe)
# print(pc.dataframe)

# for rate in [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE,
# 			cn.WEEKEND_MORNING_RATE, cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]:
# 	print(decoded[rate])


	   #  def main(argv):
    #     choice = str(sys.argv[1])
    #     output_file = str(sys.argv[3]) + '.csv'
    #     try:
    #         sys.argv[4]
    #     except:
    #         pickle_name = cn.REFERENCE_PICKLE
    #     else:
    #         pickle_name = str(sys.argv[4])
    #     if choice == "csv":
    #         # add directory where the file should be found
    #         input_file = os.path.join(PROCESSED_DIR, 'test/', str(sys.argv[2]) + '.csv')
    #         df = geocode_csv(input_file, pickle_name)
    #         write_to_csv(df, PROCESSED_DIR, output_file)
    #     elif choice == "point":
    #         coord = str(sys.argv[2])
    #         df = geocode_point(coord, pickle_name)
    #         write_to_csv(df, PROCESSED_DIR, output_file)
    #     else:
    #         raise "invalid input"


    # if __name__ == "__main__":
    #     main(sys.argv[1:])
