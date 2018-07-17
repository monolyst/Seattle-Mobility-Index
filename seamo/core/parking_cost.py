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

class ParkingCost(gbc.GeocodeBase):
    #Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
    def __init__(self):
        super().__init__()
        self.SHAPEFILE_DIR = cn.SHAPEFILE_DIR
        self.PROCESSED_DIR = cn.PROCESSED_DIR
        self.PICKLE_DIR = cn.PICKLE_DIR

    # Geocoder function
    def geocode(self, gdf, pickle_name=cn.PARKING_REFERENCE):
        """ 
        Input:  GeoPandas DataFrame gdf: cn.LAT, cn.LON
        input_file.csv needs header lat, lon
        """
        super().geocode(gdf, pickle_name)
        reference = self.get_reference(pickle_name)
        df = gpd.sjoin(gdf, reference, how = 'left')
        df = df.drop(columns = ['index_right'])
        df = pd.DataFrame(df)
        df = df.drop([cn.GEOMETRY], axis=1)
        self.dataframe = df
        return df


    def get_reference(self, pickle_name=cn.PARKING_REFERENCE):
        """
        :param str pickle_name: name of the pickle file
        :return GeoDataFrame:
        """
        gi = pci.ParkingCostInput()
        reference_gdf = gi.get_reference(self.SHAPEFILE_DIR, self.PICKLE_DIR, pickle_name)
        return reference_gdf


    def geocode_csv(self, input_file, pickle_name=cn.PARKING_REFERENCE):
        df = super().geocode_csv(input_file, pickle_name)
        return df


    def geocode_point(self, coord, pickle_name=cn.PARKING_REFERENCE):
        df = super().geocode_point(coord, pickle_name)
        return df


    def main(argv):
        choice = str(sys.argv[1])
        output_file = str(sys.argv[3]) + '.csv'
        try:
            sys.argv[4]
        except:
            pickle_name = cn.REFERENCE_PICKLE
        else:
            pickle_name = str(sys.argv[4])
        if choice == "csv":
            # add directory where the file should be found
            input_file = os.path.join(PROCESSED_DIR, 'test/', str(sys.argv[2]) + '.csv')
            df = geocode_csv(input_file, pickle_name)
            write_to_csv(df, PROCESSED_DIR, output_file)
        elif choice == "point":
            coord = str(sys.argv[2])
            df = geocode_point(coord, pickle_name)
            write_to_csv(df, PROCESSED_DIR, output_file)
        else:
            raise "invalid input"


    if __name__ == "__main__":
        main(sys.argv[1:])
