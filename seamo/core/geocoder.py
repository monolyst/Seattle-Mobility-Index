"""
Python module for the universal geocoder. Module can be called from the terminal
or imported into another script.

To run the geocoder from the terminal:
$ python geocoder.py FILE_FORTMAT INPUT OUTPUT_NAME PICKLE_NAME
- FILE_FORTMAT can be csv or point
- INPUT depends on the file format, and is either the csv name or a lat/lon pair
  in the form (LAT, LON)
- OUTPUT_NAME is the desired name to write to csv
- PICKLE_NAME (optional) include name of pickle file, default is reference.pickle

Methods can be called from other python modules based on file format passed.
Call:
- geocode(gdf, pickle_name) if passing geodataframe, pickle_name parameter
  is optional, and default value if nothing is passed is reference.pickle
- geocode_point(coord, pickle_name) if passing lat/lon pair in format (LAT, LON),
  pickle_name parameter is optional, and default value if nothing is passed is 
  reference.pickle
- geocode_csv(input_file, pickle_name) if csv passed with lat, lon header,
  pickle_name parameter is optional, and default value if nothing is passed is 
  reference.pickle
""" 
import init
import os
import sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geocoder_input
import constants as cn
import geocode_base_class as gbc

class Geocoder(gbc.GeocodeBase):
    #Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
    def __init__(self, crs=cn.CRS_EPSG):
        super().__init__(crs)


    # Geocoder function
    def geocode(self, gdf, pickle_name=cn.REFERENCE_PICKLE):
        """ 
        input_file.csv needs header lat, lon
        """
        try:
            df = super().geocode(gdf, pickle_name)
        except Exception:

        reference = self.__get_reference__(pickle_name)
        df = gpd.sjoin(gdf, reference, how = 'left')
        df = df.drop(columns = ['index_right'])
        df = df.sort_values(by=cn.GEOGRAPHY)
        df = pd.DataFrame(df)
        df = df.drop([cn.GEOMETRY], axis=1)
        df = df.set_index([cn.LAT, cn.LON, cn.GEOGRAPHY], append=cn.KEY).unstack()
        df.columns = df.columns.droplevel()
        df = self.__format_output__(df)
        self.dataframe = df
        return df


    def _format_output(self, df):
        df = df.reset_index().drop(['level_0'], axis=1)
        df[cn.LAT] = df[cn.LAT].astype(float)
        df[cn.LON] = df[cn.LON].astype(float)
        df[cn.BLOCK_GROUP] = df[cn.BLOCK_GROUP].astype(int)
        df[cn.NBHD_LONG] = df[cn.NBHD_LONG].astype(str)
        df[cn.NBHD_SHORT] = df[cn.NBHD_SHORT].astype(str)
        df[cn.COUNCIL_DISTRICT] = df[cn.COUNCIL_DISTRICT].astype(str)
        df[cn.URBAN_VILLAGE] = df[cn.URBAN_VILLAGE].astype(str)
        df[cn.ZIPCODE] = df[cn.ZIPCODE].astype(int)
        return df


    def __get_reference__(self, pickle_name=cn.REFERENCE_PICKLE):
        gi = geocoder_input.GeocoderInput()
        reference_gdf = gi.get_reference(cn.SHAPEFILE_DIR, cn.PICKLE_DIR, pickle_name)
        self.reference = reference_gdf
        return reference_gdf


    def geocode_csv(self, input_file, pickle_name=cn.REFERENCE_PICKLE):
        df = super().geocode_csv(input_file, pickle_name)
        return df


    def geocode_point(self, coord, pickle_name=cn.REFERENCE_PICKLE):
        df = super().geocode_point(coord, pickle_name)
        return df
