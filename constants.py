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
URBAN_VILLAGE = 'urban_village'
GEOMETRY = 'geometry'
KEY = 'key'
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

# Categories for basket
POST_OFFICE = 'post_office'
SUPERMARKET = 'supermarket'

# Numeric Constants
PROXIMITY_THRESHOLD = 0.8 # 5-6 miles
METERS_TO_MILES = 1609
DEG_INTO_MILES = 69
CITY_CENTER = [47.6062, -122.3321]


# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
IMPERIAL_UNITS = 'imperial'
DRIVING_MODE = 'driving'

# Google API naming
GOOGLE_LAT = 'lat'
GOOGLE_LON = 'lng' 
CLASS = 'class'
RANK = 'rank'

# Seattle Census Data naming
CENSUS_LAT = 'CT_LAT'
CENSUS_LON = 'CT_LON'
BLOCKGROUP = 'BLOCKGROUP'
BASKET_CATEGORIES = ["urban village", "citywide", "destination park", "supermarket", "library",  "hospital", "pharmacy", "post_office", "school", "cafe"]
BASKET_SIZE = 25

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
SHAPEFILE_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/shapefiles/')
PROCESSED_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/')
RAW_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/')
PICKLE_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/pickles/')
ORIGIN_FP = os.path.join(RAW_DIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.csv') 
DEST_FP = os.path.join(RAW_DIR, 'GoogleMatrix_Places_Full.csv')
