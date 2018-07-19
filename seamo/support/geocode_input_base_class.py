import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle
import constants as cn

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

    def make_reference(self, raw_dir, processed_dir, pickle_name):
        # reference = read_shapefile(raw_dir, shapefile)
        # return reference
        pass

    def make_pickle(self, processed_dir, reference, pickle_name):
        with open(os.path.join(processed_dir, str(pickle_name)), 'wb') as pickle_file:
            pickle.dump(reference, pickle_file)

    def get_reference(self, raw_dir, processed_dir, pickle_name):
        fname = processed_dir + str(pickle_name)
        try:
            reference = pickle.load(open(fname, 'rb'))
            return reference
        except:
            reference = self.make_reference(raw_dir, processed_dir, str(pickle_name))
            return reference