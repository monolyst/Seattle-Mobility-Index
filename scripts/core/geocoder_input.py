import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

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

def make_reference(DATADIR):
    blkgrp = read_shapefile('blkgrp10_shore', 'GEO_ID_GRP', 'Block_Group', DATADIR)
    nbhd_short = read_shapefile('Neighborhoods', 'S_HOOD', 'Neighborhood_Short', DATADIR)
    nbhd_long = read_shapefile('Neighborhoods', 'L_HOOD', 'Neighborhood_Long', DATADIR)
    zipcode = read_shapefile('zipcode', 'ZIPCODE', 'Zipcode', DATADIR)
    council_district = read_shapefile('sccdst', 'SCCDST', 'Seattle_City_Council_District', DATADIR)
    urban_village = read_shapefile('DPD_uvmfg_polygon', 'UV_NAME', 'Urban_Village', DATADIR)
    reference = pd.concat([blkgrp, nbhd_short, nbhd_long, zipcode, council_district, urban_village])
    return reference
