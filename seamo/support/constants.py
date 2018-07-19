"""
Constants to be used throughout the code base.
"""
import os

# Strings
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
REFERENCE_PICKLE = 'reference.pickle'

# Constants for basket
FINAL_BASKET = [1, 13, 1, 2, 1, 1, 1, 1, 3, 1] 
BASKET_SIZE = 25
URBAN_VILLAGE = 'urban_villlage'
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

CLASS = 'class'
RANK = 'rank'

# Numeric Constants
PROXIMITY_THRESHOLD_MILES = 5
METERS_TO_MILES = 1609
KM_TO_MILES = 0.621371
DEG_INTO_MILES = 69
CITY_CENTER = [47.6062, -122.3321]
EARTH_RADIUS_KM = 6373.0 # Approximate radius of Earth in km

# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
IMPERIAL_UNITS = 'imperial'
DRIVING_MODE = 'driving'
GOOGLE_DIST_MATRIX_OUT = 'google_dist_matrix_out'
TIMESTAMP = '1531933200' # Wednesday, July 18, 10AM UTC


# Google API naming
GOOGLE_PLACES_LAT = 'lat'
GOOGLE_PLACES_LON = 'lng' 
GOOGLE_START_LAT = 'start_lat'
GOOGLE_START_LON = 'start_lon'
GOOGLE_END_LAT = 'end_lat'
GOOGLE_END_LON = 'end_lon'
PLACE_ID = 'place_id'

# Seattle Census Data naming
CENSUS_LAT = 'CT_LAT'
CENSUS_LON = 'CT_LON'
BLOCKGROUP = 'BLOCKGROUP'

# Parameter domains
AA = [0,1,2,3,4] # urban village
BB = [8,9,10,11,12,13] # citywide destination
A = [0,1,2,3] # destination park
B = [0,1,2,3] # supermarket
C = [0,1,2,3] # library
D = [0,1,2,3] # hospital
E = [0,1,2,3] # pharmacy
F = [0,1,2,3] # post office
G = [0,1,2,3] # school
H = [0,1,2,3] # cafe

# Filepaths
DATADIR = 'data/'
SHAPEFILE_DIR = os.path.join(DATADIR, 'raw/shapefiles/')
PROCESSED_DIR = os.path.join(DATADIR, 'processed/')
RAW_DIR = os.path.join(DATADIR, 'raw/')
PICKLE_DIR = os.path.join(PROCESSED_DIR, 'pickles/')
ORIGIN_FP = os.path.join(RAW_DIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv') 
DEST_FP = os.path.join(RAW_DIR, 'GoogleMatrix_Places_Full.csv')
GOOGLE_DIST_FP = os.path.join(RAW_DIR, 'GoogleMatrix_Dist_Out.csv')
DB_DIR = os.path.join(PROCESSED_DIR, 'databases/')
CSV_DIR = os.path.join(PROCESSED_DIR, 'csv_files/')
HAVERSINE_DIST_FP = os.path.join(CSV_DIR, 'haversine_distances.csv')
API_DIST_FP = os.path.join(CSV_DIR, 'api_distances.csv')
RANKED_DEST_FP = os.path.join(CSV_DIR, 'ranked_destinations.csv')
BASKETS_FP = os.path.join(CSV_DIR, 'input_baskets.csv')
