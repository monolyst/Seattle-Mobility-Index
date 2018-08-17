import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle
import constants as cn
import data_accessor as daq

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

class GeocodeInputBase(object):
    def __init__(self):
        self.reference = None
        self.pickle_name = None
        self.raw_dir = None
        self.processed_dir = None


    def read_shapefile(self, raw_dir, shapefile):
        shapefile = str(shapefile) + '.shp'
        gdf = gpd.read_file(os.path.join(raw_dir, shapefile))
        return gdf


    def make_pickle(self, processed_dir, reference, pickle_name):
        daq.make_pickle(processed_dir, reference, pickle_name)


    def get_reference(self, raw_dir, processed_dir, pickle_name):
        try:
            daq.open_pickle(processed_dir, pickle_name)
        except:
            return self.make_reference(raw_dir, processed_dir, str(pickle_name))
        else:
            return daq.open_pickle(processed_dir, pickle_name)