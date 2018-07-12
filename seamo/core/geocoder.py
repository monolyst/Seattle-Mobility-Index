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
import __init__
import os
import sys
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import geocoder_input as gi
import constants as cn

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
SHAPEFILE_DIR = cn.SHAPEFILE_DIR
PROCESSED_DIR = cn.PROCESSED_DIR
PICKLE_DIR = cn.PICKLE_DIR

#Geocoder function
def geocode(gdf, pickle_name=cn.REFERENCE_PICKLE):
    """ 
    input_file.csv needs header lat, lon
    """
    reference = get_reference(pickle_name)
    df = gpd.sjoin(gdf, reference, how = 'left')
    df = df.drop(columns = ['index_right'])
    df = df.sort_values(by=cn.GEOGRAPHY)
    df = pd.DataFrame(df)
    df = df.drop([cn.GEOMETRY], axis=1)
    df = df.set_index([cn.LAT, cn.LON, cn.GEOGRAPHY], append=cn.KEY).unstack()
    df.columns = df.columns.droplevel()
    # values = {'Block_Group': 0, 'Neighborhood_Long': 'N/A', 'Neighborhood_Short': 'N/A',
    #           'Seattle_City_Council_District': 'N/A', 'Urban_Village': 'N/A', 'Zipcode': 0}
    # df = df.fillna(value=values)
    df = format_output(df)
    return df


def format_output(df):
    df = df.reset_index().drop(['level_0'], axis=1)
    df[cn.LAT] = df[cn.LAT].astype(float)
    df[cn.LON] = df[cn.LON].astype(float)
    df[cn.BLOCK_GROUP] = df[cn.BLOCK_GROUP].astype(np.int64)
    df[cn.NBHD_LONG] = df[cn.NBHD_LONG].astype(str)
    df[cn.NBHD_SHORT] = df[cn.NBHD_SHORT].astype(str)
    df[cn.COUNCIL_DISTRICT] = df[cn.COUNCIL_DISTRICT].astype(str)
    df[cn.URBAN_VILLAGE] = df[cn.URBAN_VILLAGE].astype(str)
    df[cn.ZIPCODE] = df[cn.ZIPCODE].astype(np.int64)
    return df


def get_reference(pickle_name=cn.REFERENCE_PICKLE):
    reference = gi.get_reference(SHAPEFILE_DIR, PICKLE_DIR, pickle_name)
    return reference


def geocode_csv(input_file, pickle_name=cn.REFERENCE_PICKLE):
    data = pd.read_csv(str(input_file))
    data[cn.GEOMETRY] = data.apply(lambda x: Point((float(x[1]), float(x[0]))), axis=1)
    data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
    data.crs = cn.CRS_EPSG
    df = geocode(data, str(pickle_name))
    return df


def geocode_point(coord, pickle_name=cn.REFERENCE_PICKLE):
    left, right = split_coord(coord)
    data = pd.DataFrame(data={cn.LAT: [left], cn.LON: [right],
        cn.GEOMETRY: [Point((float(right), float(left)))]})
    data = data[[cn.LAT, cn.LON, cn.GEOMETRY]]
    data = gpd.GeoDataFrame(data, geometry=cn.GEOMETRY)
    data.crs = cn.CRS_EPSG
    df = geocode(data, str(pickle_name))
    return df


def split_coord(coord):
    coord = str(coord).split(", ")
    left = coord[0][1:]
    right = coord[1][:-1]
    return left, right


def write_to_csv(df, PROCESSED_DIR, output_file):
    decoded = df
    decoded.to_csv(PROCESSED_DIR + output_file, index=False)


def main(argv):
    CHOICE = str(sys.argv[1])
    output_file = str(sys.argv[3]) + '.csv'
    try:
        sys.argv[4]
    except:
        pickle_name = cn.REFERENCE_PICKLE
    else:
        pickle_name = str(sys.argv[4])
    if CHOICE == "csv":
        # add directory where the file should be found
        input_file = os.path.join(PROCESSED_DIR, 'test/', str(sys.argv[2]) + '.csv')
        df = geocode_csv(input_file, pickle_name)
        write_to_csv(df, PROCESSED_DIR, output_file)
    elif CHOICE == "point":
        coord = str(sys.argv[2])
        df = geocode_point(coord, pickle_name)
        write_to_csv(df, PROCESSED_DIR, output_file)
    else:
        raise "invalid input"


if __name__ == "__main__":
    main(sys.argv[1:])
