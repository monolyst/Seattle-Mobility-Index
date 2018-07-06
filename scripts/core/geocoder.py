"""
command to run script is $ python geocoder.py FILE_FORTMAT INPUT OUTPUT_NAME PICKLE_NAME
""" 
import os
import sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geocoder_input as gi

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
DATADIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/shapefiles/')
PROCESSED_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/')
PICKLE_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/pickles/')

#Geocoder function
def geocode(gdf, pickle_name="reference.pickle"):
    """ 
    input_file.csv needs header lat, lon
    """
    reference = get_reference(pickle_name)
    df = gpd.sjoin(gdf, reference, how = 'left')
    df = df.drop(columns = ['index_right'])
    df = df.sort_values(by='geography')
    df = pd.DataFrame(df)
    df = df.drop(['geometry'],axis=1)
    df = df.set_index(['lat', 'lon','geography'], append='key').unstack()
    df.columns = df.columns.droplevel()
    values = {'Block_Group': 'N/A', 'Neighborhood_Long': 'N/A', 'Neighborhood_Short': 'N/A',
              'Seattle_City_Council_District': 'N/A', 'Urban_Village': 'N/A', 'Zipcode': 'N/A'}
    df = df.fillna(value=values)
    return df


def get_reference(pickle_name="reference.pickle"):
    reference = gi.get_reference(DATADIR, PICKLE_DIR, pickle_name)
    return reference


def geocode_csv(input_file, pickle_name="reference.pickle"):
    data = pd.read_csv(str(input_file))
    data['geometry'] = data.apply(lambda x: Point((float(x[1]), float(x[0]))), axis=1)
    data = gpd.GeoDataFrame(data, geometry='geometry')
    data.crs = {'init': 'epsg:4326'}
    df = geocode(data, pickle_name)
    return df


def geocode_point(coord, pickle_name="reference.pickle"):
    coord = str(coord).split(", ")
    left = coord[0][1:]
    right = coord[1][:-1]
    data = pd.DataFrame(data={'lat': [left], 'lon': [right],
        'geometry': [Point((float(right), float(left)))]})
    data = data[['lat', 'lon', 'geometry']]
    data = gpd.GeoDataFrame(data, geometry='geometry')
    data.crs = {'init': 'epsg:4326'}
    df = geocode(data, pickle_name)
    return df


def write_to_csv(df, PROCESSED_DIR, output_file):
    decoded = df
    decoded.to_csv(PROCESSED_DIR + output_file)


def main(argv):
    CHOICE = str(sys.argv[1])
    output_file = str(sys.argv[3]) + '.csv'
    pickle_name = str(sys.argv[4])
    if CHOICE == "csv":
        # add directory where the file should be found
        input_file = '../../seamo/data/test/' + str(sys.argv[2]) + '.csv'
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
