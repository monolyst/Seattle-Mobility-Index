"""
Constants to be used throughout the code base.
"""
import itertools
import os
import numpy as np

# Strings

# Constants for basket
FINAL_BASKET = [1, 13, 1, 2, 1, 1, 1, 1, 3, 1]
BASKET_SIZE = 25
URBAN_VILLAGE = 'urban_village'
CITYWIDE = 'citywide'
DESTINATION_PARK = 'destination_park'
SUPERMARKET = 'supermarket'
LIBRARY = 'library'
HOSPITAL = 'hospital'
PHARMACY = 'pharmacy'
POST_OFFICE = 'post_office'
SCHOOL = 'school'
CAFE = 'cafe'
BASKET_CATEGORIES = [URBAN_VILLAGE,
                    CITYWIDE,
                    DESTINATION_PARK,
                    SUPERMARKET,
                    LIBRARY,
                    HOSPITAL,
                    PHARMACY,
                    POST_OFFICE,
                    SCHOOL,
                    CAFE]

# Ranges of counts for each class of destination
AA = [1,2,3,4] # urban village
BB = [8,9,10,11,12,13] # citywide destination
A = [1,2,3] # destination park
B = [1,2,3] # supermarket
C = [1,2,3] # library
D = [1,2,3] # hospital
E = [1,2,3] # pharmacy
F = [1,2,3] # post office
G = [1,2,3] # school
H = [1,2,3] # cafe

# Cartesian product. Iterates through all possible basket combinations. 
BASKET_COMBOS = itertools.product(AA, BB, A, B, C, D, E, F, G, H) 

CLASS = 'class'
RANK = 'rank'

# Column Names
DISTANCE = 'distance'
LAT = 'lat'
LON = 'lon'
PAIR = 'pair'
BLOCK_GROUP = 'block_group'
NBHD_LONG = 'neighborhood_long'
NBHD_SHORT = 'neighborhood_short'
COUNCIL_DISTRICT = 'seattle_city_council_district'
ZIPCODE = 'zipcode'
GEOMETRY = 'geometry'
KEY = 'key'
GEOGRAPHY = 'geography'
CRS_EPSG = {'init' :'epsg:4326'}
SHAPE_AREA = 'Shape_area'
AREA = 'area'
# Columns specific to basket eval
VERT_HORI_RATIO = 'vert_hori_ratio'
PROX_RATIO = 'proximity_ratio'
AVG_DIST = 'average_distance'
DIST_CITY_CENTER = 'dist_from_city_center'


# Parking
BLOCK_FACE = 'block_face'
BLOCK_NUMBER = 'block_number'
PARKING_CATEGORY = 'parking_category'
WEEKDAY_MORNING_RATE = 'weekday_morning_rate'
WEEKDAY_AFTERNOON_RATE = 'weekday_afternoon_rate'
WEEKDAY_EVENING_RATE = 'weekday_evening_rate'
WEEKDAY_MORNING_START = 'weekday_morning_start'
WEEKDAY_AFTERNOON_START = 'weekday_afternoon_start'
WEEKDAY_EVENING_START = 'weekday_evening_start'
WEEKDAY_MORNING_END = 'weekday_morning_end'
WEEKDAY_AFTERNOON_END = 'weekday_afternoon_end'
WEEKDAY_EVENING_END = 'weekday_evening_end'
WEEKEND_MORNING_RATE = 'weekend_morning_rate'
WEEKEND_AFTERNOON_RATE = 'weekend_afternoon_rate'
WEEKEND_EVENING_RATE = 'weekend_evening_rate'
WEEKEND_MORNING_START = 'weekend_morning_start'
WEEKEND_AFTERNOON_START = 'weekend_afternoon_start'
WEEKEND_EVENING_START = 'weekend_evening_start'
WEEKEND_MORNING_END = 'weekend_morning_end'
WEEKEND_AFTERNOON_END = 'weekend_afternoon_end'
WEEKEND_EVENING_END = 'weekend_evening_end'
BUFFER_SIZE = 0.0005
PARKING_COLUMNS = ['BLOCK_NBR', 'PARKING_CA', 'WKD_RATE1', 'WKD_RATE2', 'WKD_RATE3',
                'WKD_START1', 'WKD_END1', 'WKD_START2', 'WKD_END2', 'WKD_START3',
                'WKD_END3', 'SAT_RATE1', 'SAT_RATE2', 'SAT_RATE3', 'SAT_START1',
                'SAT_END1', 'SAT_START2', 'SAT_END2', 'SAT_START3', 'SAT_END3', GEOMETRY]
NO_PARKING_ALLOWED = 'No Parking Allowed'
RATE = 'rate'


# geocode exception handling
GEOCODE_NAN_DF = {LAT:[np.nan], LON:[np.nan], BLOCK_GROUP:[np.nan],
                NBHD_LONG:[np.nan], NBHD_SHORT:[np.nan], COUNCIL_DISTRICT:[np.nan],
                URBAN_VILLAGE:[np.nan], ZIPCODE:[np.nan]}

PARKING_NAN_DF = {BLOCK_NUMBER: [np.nan], PARKING_CATEGORY:[np.nan], WEEKDAY_MORNING_RATE:[np.nan],
                WEEKDAY_AFTERNOON_RATE:[np.nan], WEEKDAY_EVENING_RATE:[np.nan], WEEKDAY_MORNING_START:[np.nan],
                WEEKDAY_MORNING_END:[np.nan], WEEKDAY_AFTERNOON_START:[np.nan], WEEKDAY_AFTERNOON_END:[np.nan],
                WEEKDAY_EVENING_START:[np.nan], WEEKDAY_EVENING_END:[np.nan], WEEKEND_MORNING_RATE:[np.nan],
                WEEKEND_AFTERNOON_RATE:[np.nan], WEEKEND_EVENING_RATE:[np.nan], WEEKEND_MORNING_START:[np.nan],
                WEEKEND_MORNING_END:[np.nan], WEEKEND_AFTERNOON_START:[np.nan], WEEKEND_AFTERNOON_END:[np.nan],
                WEEKEND_EVENING_START:[np.nan], WEEKEND_EVENING_END:[np.nan]}

# Seattle Polygon

# Shapefiles
BLKGRP_FNAME = 'blkgrp10_shore'
BLKGRP_KEY = 'GEO_ID_GRP'
NBHD_FNAME = 'Neighborhoods'
NBHD_SHORT_KEY = 'S_HOOD'
NBHD_LONG_KEY = 'L_HOOD'
ZIPCODE_FNAME = 'zipcode'
ZIPCODE_KEY = 'ZIPCODE'
COUNCIL_DISTRICT_FNAME = 'sccdst'
COUNCIL_DISTRICT_KEY = 'SCCDST'
URBAN_VILLAGE_FNAME = 'DPD_uvmfg_polygon'
URBAN_VILLAGE_KEY = 'UV_NAME'
BLOCK_FACE_FNAME = 'Blockface'
REFERENCE_PICKLE = 'reference.pickle'
PARKING_REFERENCE = 'parking_reference.pickle'

# Numeric Constants
BASKET_EVAL_PROX_MIN = 2 # 2 miles
BASKET_EVAL_PROX_MAX = 10 # 10 miles
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles in lat-long coords
METERS_TO_MILES = 1609
KM_TO_MILES = 0.621371
DEG_INTO_MILES = 69
MIN_TO_HR = 60
CITY_CENTER = [47.6062, -122.3321]
EARTH_RADIUS_KM = 6373.0 # Approximate radius of Earth in km
AAA_RATE = 0.56
VOT_RATE = 14.10
BIKE_RATE = 0.15

# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
IMPERIAL_UNITS = 'imperial'
DRIVING_MODE = 'driving'
GOOGLE_DIST_MATRIX_OUT = 'google_dist_matrix_out'
TIMESTAMP = '1531933200' # Wednesday, July 18, 10AM UTC
API_CALL_LIMIT = 100000

# Google API and distance data column naming
GOOGLE_PLACES_LAT = 'lat'
GOOGLE_PLACES_LON = 'lng'
GOOGLE_START_LAT = 'start_lat'
GOOGLE_START_LON = 'start_lon'
GOOGLE_END_LAT = 'end_lat'
GOOGLE_END_LON = 'end_lon'
PLACE_ID = 'place_id'
ORIGIN = 'origin'
DESTINATION = 'destination'
DESTINATIONS = 'destinations'
PLACE_IDS = 'place_ids'

# Seattle Census Data naming
CENSUS_LAT = 'CT_LAT'
CENSUS_LON = 'CT_LON'
BLOCKGROUP = 'BLOCKGROUP'


# Directory paths
DATADIR = 'data/'
RAW_DIR = os.path.join(DATADIR, 'raw/')
SHAPEFILE_DIR = os.path.join(RAW_DIR, 'shapefiles/')
PROCESSED_DIR = os.path.join(DATADIR, 'processed/')
PICKLE_DIR = os.path.join(PROCESSED_DIR, 'pickles/')
DB_DIR = os.path.join(PROCESSED_DIR, 'databases/')
CSV_DIR = os.path.join(PROCESSED_DIR, 'csv_files/')
TEST_DIR = os.path.join(DATADIR, 'test/')
GEN_SHAPEFILE_DIR = os.path.join(PROCESSED_DIR, 'shapefiles/')
# Filepaths
ORIGIN_FP = os.path.join(RAW_DIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv')
DEST_FP = os.path.join(RAW_DIR, 'GoogleMatrix_Places_Full.csv')
GOOGLE_DIST_FP = os.path.join(RAW_DIR, 'GoogleMatrix_Dist_Out.csv')
HAVERSINE_DIST_FP = os.path.join(CSV_DIR, 'haversine_distances.csv')
DISTANCE_QUEUE_FP = os.path.join(CSV_DIR, 'distance_queue.csv')
API_DIST_FP = os.path.join(CSV_DIR, 'api_distances.csv')
RANKED_DEST_FP = os.path.join(CSV_DIR, 'ranked_destinations.csv')
BASKETS_FP = os.path.join(CSV_DIR, 'baskets.csv')
INPUT_BASKETS_FP = os.path.join(CSV_DIR, 'input_baskets.csv')
BASKET_COMBO_FP = os.path.join(CSV_DIR, 'basket_combinations.csv')
MSES_FP = os.path.join(CSV_DIR, 'basket_mses.csv')
PSRC_FP = os.path.join(RAW_DIR, 'PSRC_full_final.csv')
