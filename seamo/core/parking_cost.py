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
import numpy as np
from shapely.geometry import Point
import parking_cost_input as pci
import constants as cn
import geocode_base_class as gbc
import support.seamo_exceptions as se
import coordinate

class ParkingCost(gbc.GeocodeBase):
    #Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
    def __init__(self, crs=cn.CRS_EPSG):
        super().__init__(crs)


    # Geocoder function
    def geocode(self, gdf, pickle_name):
        """ 
        Input:  GeoPandas DataFrame gdf: cn.LAT, cn.LON
        input_file.csv needs header lat, lon
        """
        reference_gdf = self._get_parking_reference(pickle_name)
        try:
            self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        except se.NoOverlapSpatialJoinError as e:
            print('No overlap found')
            df = pd.DataFrame(cn.PARKING_NAN_DF)
            raise se.NoParkingAvailableError("No Parking Available")
        else:
            df = self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        self.dataframe = df
        return df


    def _get_parking_reference(self, pickle_name):
        """
        :param str pickle_name: name of the pickle file
        :return GeoDataFrame:
        """
        gi = pci.ParkingCostInput()
        return self._get_reference(pickle_name, gi)


    def geocode_csv(self, input_file, pickle_name):
        return super().geocode_csv(input_file, pickle_name)


    def geocode_point(self, coord):
        df = super().geocode_point(coord)
        point = coordinate.Coordinate(df[cn.LAT], df[cn.LON])
        pickle_name = {cn.COUNCIL_DISTRICT1: cn.DISTRICT1_PICKLE,
                    cn.COUNCIL_DISTRICT2: cn.DISTRICT2_PICKLE,
                    cn.COUNCIL_DISTRICT3: cn.DISTRICT3_PICKLE,
                    cn.COUNCIL_DISTRICT4: cn.DISTRICT4_PICKLE,
                    cn.COUNCIL_DISTRICT5: cn.DISTRICT5_PICKLE,
                    cn.COUNCIL_DISTRICT6: cn.DISTRICT6_PICKLE,
                    cn.COUNCIL_DISTRICT7: cn.DISTRICT7_PICKLE}[point.council_district]
        return self.geocode(df, str(pickle_name))
