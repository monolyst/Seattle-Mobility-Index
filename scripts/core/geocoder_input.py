import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle
import contants as cn

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

def read_shapefile(shapefile, column_name, name, DATADIR):
    shapefile = str(shapefile) + '.shp'
    geography = gpd.read_file(os.path.join(DATADIR, shapefile))
    geography = geography.loc[:, (column_name, cn.GEOMETRY)]
    geography = geography.to_crs(cn.CRS_EPSG)
    geography.columns = [cn.KEY, cn.GEOMETRY]
    geography[cn.GEOGRAPHY] = str(name)
    return geography

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

def make_pickle(directory, reference, pickle_name):
    with open(os.path.join(directory, str(pickle_name)), 'wb') as pickle_file:
        pickle.dump(reference, pickle_file)

def get_reference(DATADIR, directory, pickle_name):
    fname = directory + str(pickle_name)
    try:
        reference = pickle.load(open(fname, 'rb'))
        return reference
    except:
        reference = make_reference(DATADIR, directory, str(pickle_name))
        return reference