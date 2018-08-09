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
import numpy as np
import geocoder_input
import constants as cn
import geocode_base_class as gbc
import support.seamo_exceptions as se

class Geocoder(gbc.GeocodeBase):
    #Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
    def __init__(self, crs=cn.CRS_EPSG):
        super().__init__(crs)


    # Geocoder function
    def geocode(self, gdf, pickle_name=cn.REFERENCE_PICKLE):
        """ 
        input_file.csv needs header lat, lon
        """
        reference_gdf = self._get_geocode_reference(0, pickle_name)
        try:
            self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        except se.NoOverlapSpatialJoinError:
            # print('No overlap found')
            df = pd.DataFrame(cn.GEOCODE_NAN_DF)
        else:
            df = self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
            df = df.sort_values(by=cn.GEOGRAPHY)
            df = df.set_index([cn.LAT, cn.LON, cn.GEOGRAPHY], append=cn.KEY).unstack()
            df.columns = df.columns.droplevel()
            # print(df)
            df = self._format_output(df)
        self.dataframe = df
        return df


    def geocode_blockgroup(self, gdf, pickle_name=cn.BLOCKGROUP_PICKLE):
        reference_gdf = self._get_geocode_reference(1, pickle_name)
        # import pdb; pdb.set_trace()
        try:
            self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        except se.NoOverlapSpatialJoinError:
            print('No overlap found')
            df = pd.DataFrame({cn.KEY: [None]})
        else:
            df = self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
            df[cn.KEY] = df[cn.KEY].astype(str)
        return df


    def _format_output(self, df):
        df = df.reset_index().drop(['level_0'], axis=1)
        df[cn.LAT] = df[cn.LAT].astype(float)
        df[cn.LON] = df[cn.LON].astype(float)
        for col in [cn.BLOCK_GROUP, cn.NBHD_LONG, cn.NBHD_SHORT, cn.COUNCIL_DISTRICT,
                    cn.URBAN_VILLAGE, cn.ZIPCODE]:
            try:
                df[col].astype(str)
            except KeyError:
                df[col] = None
            else:
                df[col] = df[col].astype(str)
        df = df[[cn.LAT, cn.LON, cn.BLOCK_GROUP, cn.NBHD_LONG, cn.NBHD_SHORT,cn.COUNCIL_DISTRICT,
                cn.URBAN_VILLAGE, cn.ZIPCODE]]
        return df


    def _get_geocode_reference(self, ref_type, pickle_name):
        if ref_type == 0:
            gi = geocoder_input.GeocoderInput()
            return self._get_reference(pickle_name, gi)
        elif ref_type == 1:
            gi = geocoder_input.GeocoderBlockgroupInput()
            return self._get_reference(pickle_name, gi)


    def geocode_csv(self, input_file, pickle_name=cn.REFERENCE_PICKLE):
        return super().geocode_csv(input_file, pickle_name)


    def geocode_point(self, coord, pickle_name=cn.REFERENCE_PICKLE):
        df = super().geocode_point(coord) 
        return self.geocode(df, str(pickle_name))

    def geocode_df(self, df, pickle_name=cn.REFERENCE_PICKLE):
        df = super().geocode_df(df)
        return self.geocode(df, str(pickle_name))

    def get_blockgroup_from_point(self, coord, pickle_name=cn.BLOCKGROUP_PICKLE):
        df = super().geocode_point(coord) 
        return self.geocode_blockgroup(df, str(pickle_name))

    def get_blockgroup_from_df(self, df, pickle_name=cn.BLOCKGROUP_PICKLE):
        df = super().geocode_df(df)
        return self.geocode_blockgroup(df, str(pickle_name))
