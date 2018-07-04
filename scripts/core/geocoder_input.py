import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

def read_shapefile(shapefile, column_name, name, DATADIR):
    shapefile = str(shapefile) + '.shp'
    geography = gpd.read_file(os.path.join(DATADIR, shapefile))
    geography = geography.loc[:, (column_name, 'geometry')]
    geography = geography.to_crs({'init' :'epsg:4326'})
    geography.columns = ['key', 'geometry']
    geography['geography'] = str(name)
    return geography

def make_reference(DATADIR, directory):
    blkgrp = read_shapefile('blkgrp10_shore', 'GEO_ID_GRP', 'Block_Group', DATADIR)
    nbhd_short = read_shapefile('Neighborhoods', 'S_HOOD', 'Neighborhood_Short', DATADIR)
    nbhd_long = read_shapefile('Neighborhoods', 'L_HOOD', 'Neighborhood_Long', DATADIR)
    zipcode = read_shapefile('zipcode', 'ZIPCODE', 'Zipcode', DATADIR)
    council_district = read_shapefile('sccdst', 'SCCDST', 'Seattle_City_Council_District', DATADIR)
    urban_village = read_shapefile('DPD_uvmfg_polygon', 'UV_NAME', 'Urban_Village', DATADIR)
    reference = pd.concat([blkgrp, nbhd_short, nbhd_long, zipcode, council_district, urban_village])
    make_pickle(directory, reference)
    return reference

def make_pickle(directory, reference):
    with open(os.path.join(directory, "reference.pickle"), 'wb') as pickle_file:
        pickle.dump(reference, pickle_file)
        return

def get_reference(DATADIR, directory, pickle_name):
    pickle_name = str(pickle_name)
    fname = directory + pickle_name
    if os.path.isfile(fname):
        reference = pickle.load(open(fname, 'rb'))
        return reference
    else:
        make_reference(DATADIR, directory)