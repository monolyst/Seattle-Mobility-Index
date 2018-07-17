import init
import os
import sys
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import geocode_input_base_class as gib
import constants as cn

class GeocodeBase(object):
    def __init__(self):
        self.dataframe = None
        self.pickle_name = None
        self.reference = None

    def geocode(self, gdf, pickle_name):
        """ 
        input_file.csv needs header lat, lon
        """
        # reference = get_reference(pickle_name)
        # df = gpd.sjoin(gdf, reference, how = 'left')
        # df = df.drop(columns = ['index_right'])
        # return df
        


    def get_reference(self, pickle_name):
        gi = gib.GeocodeInputBase()
        # reference = gi.get_reference(SHAPEFILE_DIR, PICKLE_DIR, pickle_name)
        # return reference



    def geocode_csv(self, input_file, pickle_name):
        data = pd.read_csv(str(input_file))
        data[cn.GEOMETRY] = data.apply(lambda x: Point((float(x[1]), float(x[0]))), axis=1)
        data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
        data.crs = cn.CRS_EPSG
        df = self.geocode(data, str(pickle_name))
        return df


    def geocode_point(self, coord, pickle_name):
        # import pdb; pdb.set_trace()
        left, right = self.split_coord(coord)
        data = pd.DataFrame(data={cn.LAT: [left], cn.LON: [right], cn.GEOMETRY:
            [Point((float(right), float(left)))]})
        data = data[[cn.LAT, cn.LON, cn.GEOMETRY]]
        data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
        data.crs = cn.CRS_EPSG
        df = self.geocode(data, str(pickle_name))
        return df


    def split_coord(self, coord):
        coord = str(coord).split(", ")
        left = coord[0][1:]
        right = coord[1][:-1]
        return left, right


    def write_to_csv(self, df, PROCESSED_DIR, output_file):
        decoded = df
        decoded.to_csv(PROCESSED_DIR + output_file, index=False)