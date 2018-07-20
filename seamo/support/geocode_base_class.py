import init
import os
import sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geocode_input_base_class as gib
import constants as cn

class GeocodeBase(object):
    def __init__(self, crs):
        self.dataframe = None
        self.pickle_name = None
        self.reference = None
        self.crs = crs

    def geocode(self, gdf, pickle_name):
        """ 
        input_file.csv needs header lat, lon
        """
        self.pickle_name = pickle_name
        reference = get_reference(pickle_name)
        try:
            df = gpd.sjoin(gdf, reference, how = 'left')
        except:
            raise exception

        df = df.drop(columns = ['index_right'])
        return df
        


    def _get_reference(self, pickle_name):
        gi = gib.GeocodeInputBase()
        # reference = gi.get_reference(SHAPEFILE_DIR, PICKLE_DIR, pickle_name)
        # return reference



    def geocode_csv(self, input_file, pickle_name):
        data = pd.read_csv(str(input_file))
        data[cn.GEOMETRY] = data.apply(lambda x: Point((float(x[1]), float(x[0]))), axis=1)
        data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
        data.crs = self.crs
        df = self.geocode(data, str(pickle_name))
        return df


    def geocode_point(self, coord, pickle_name):
        left, right = self.__split_coord__(coord)
        data = pd.DataFrame(data={cn.LAT: [left], cn.LON: [right], cn.GEOMETRY:
            [Point((float(right), float(left)))]})
        data = data[[cn.LAT, cn.LON, cn.GEOMETRY]]
        data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
        data.crs = self.crs
        df = self.geocode(data, str(pickle_name))
        return df


    def __split_coord__(self, coord):
        coord = str(coord).split(", ")
        left = coord[0][1:]
        right = coord[1][:-1]
        return left, right


    def write_to_csv(self, df, processed_dir, output_file):
        decoded = df
        decoded.to_csv(processed_dir + output_file, index=False)