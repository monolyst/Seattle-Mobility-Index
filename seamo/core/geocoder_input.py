import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import pickle
import constants as cn

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

def read_shapefile(shapefile, column_name, name, DATADIR,
    reference_type=cn.BLOCK_GROUP):
    shapefile = str(shapefile) + '.shp'
    gdf = gpd.read_file(os.path.join(DATADIR, shapefile))
    if reference_type == cn.BLOCK_GROUP:
        geography = gdf.loc[:, (column_name, cn.GEOMETRY)]
        geography = geography.to_crs(cn.CRS_EPSG)
        geography.columns = [cn.KEY, cn.GEOMETRY]
        geography[cn.GEOGRAPHY] = str(name)
        return geography

    elif reference_type == cn.BLOCK_FACE:
        for col in gdf:
            # get dtype for column
            col_type = gdf[col].dtype 
            # check if it is a number
            if col_type == int or col_type == float:
                gdf[col].fillna(0, inplace=True)
            else:
                gdf[col].fillna('None', inplace=True)
        parking = gdf.loc[:, (column_name, cn.PARKING_CATEGORY, cn.WEEKDAY_MORNING_RATE,
            cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE, cn.WEEKDAY_MORNING_START,
            cn.WEEKDAY_AFTERNOON_START, cn.WEEKDAY_EVENING_START, cn.WEEKDAY_MORNING_END,
            cn.WEEKDAY_AFTERNOON_END, cn.WEEKDAY_EVENING_END, cn.WEEKEND_MORNING_RATE,
            cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE, cn.WEEKEND_MORNING_START,
            cn.WEEKEND_AFTERNOON_START, cn.WEEKEND_EVENING_START, cn.WEEKEND_MORNING_END,
            cn.WEEKEND_AFTERNOON_END, cn.WEEKEND_EVENING_END, cn.GEOMETRY)]
        parking.crs = cn.CRS_EPSG
        return parking

def make_reference(DATADIR, directory, pickle_name):
    blkgrp = read_shapefile(cn.BLKGRP_FNAME, cn.BLKGRP_KEY, cn.BLOCK_GROUP, DATADIR)
    nbhd_short = read_shapefile(cn.NBHD_FNAME, cn.NBHD_SHORT_KEY, cn.NBHD_SHORT, DATADIR)
    nbhd_long = read_shapefile(cn.NBHD_FNAME, cn.NBHD_LONG_KEY, cn.NBHD_LONG, DATADIR)
    zipcode = read_shapefile(cn.ZIPCODE_FNAME, cn.ZIPCODE_KEY, cn.ZIPCODE, DATADIR)
    council_district = read_shapefile(cn.COUNCIL_DISTRICT_FNAME, cn.COUNCIL_DISTRICT_KEY, cn.COUNCIL_DISTRICT, DATADIR)
    urban_village = read_shapefile(cn.URBAN_VILLAGE_FNAME, cn.URBAN_VILLAGE_KEY, cn.URBAN_VILLAGE, DATADIR)
    reference = pd.concat([blkgrp, nbhd_short, nbhd_long, zipcode, council_district, urban_village])
    make_pickle(directory, reference, pickle_name)
    return reference

def make_parking_reference(DATADIR, directory, pickle_name):
    reference = read_shapefile(cn.BLOCK_FACE_FNAME, cn.BLOCK_NUMBER, cn.BLOCK_FACE, DATADIR, cn.BLOCK_FACE)
    intervals = [cn.WEEKDAY_MORNING_START, cn.WEEKDAY_AFTERNOON_START, cn.WEEKDAY_EVENING_START,
        cn.WEEKDAY_MORNING_END, cn.WEEKDAY_AFTERNOON_END, cn.WEEKDAY_EVENING_END,
        cn.WEEKEND_MORNING_START, cn.WEEKEND_AFTERNOON_START, cn.WEEKEND_EVENING_START,
        cn.WEEKEND_MORNING_END, cn.WEEKEND_AFTERNOON_END,cn.WEEKEND_EVENING_END]
    for interval in intervals:
        reference[interval] = reference[interval].apply(lambda x: int(x/60) if pd.notnull(x) else x)
        reference[interval] = reference[interval].apply(lambda x: x if x != 0 else np.nan)

    # Make a copy of the blockface geoDataFrame because buffer replaces the geometry column with the buffer polygons
    print(type(reference.geometry))
    # import pdb; pdb.set_trace()
    parking_buff = reference.copy()
    #The distance value is in degrees beucase we are using epsg4326. 
    parking_buff.geometry = reference.geometry.buffer(0.0001) 

    make_pickle(directory, parking_buff, pickle_name)
    return parking_buff

def make_pickle(directory, reference, pickle_name):
    with open(os.path.join(directory, str(pickle_name)), 'wb') as pickle_file:
        pickle.dump(reference, pickle_file)

def check_exists(DATADIR, directory, pickle_name, method):
    fname = directory + str(pickle_name)
    try:
        reference = pickle.load(open(fname, 'rb'))
        return reference
    except:
        reference = method(DATADIR, directory, str(pickle_name))
        return reference

def get_reference(DATADIR, directory, pickle_name, reference_type=cn.BLOCK_GROUP):
    # import pdb; pdb.set_trace()
    if reference_type == cn.BLOCK_GROUP:
        reference = check_exists(DATADIR, directory, pickle_name, make_reference)
        return reference
    elif reference_type == cn.BLOCK_FACE:
        reference = check_exists(DATADIR, directory, pickle_name, make_parking_reference)
        return reference
