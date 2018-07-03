"""
command to run script is $ python geopandas_geocoder csv_file output_name
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

#Geocoder function
def geocode(input_file, reference):
    """ 
    input_file.csv needs header lat, lon
    """
    data = pd.read_csv(input_file)
    
    data['geometry'] = data.apply(lambda x: Point((float(x[1]), float(x[0]))), axis=1)
    data = gpd.GeoDataFrame(data, geometry='geometry')
    data.crs = {'init' :'epsg:4326'}
                                 
    df = gpd.sjoin(data, reference, how = 'inner')
    df = df.drop(columns = ['index_right'])
    df = df.sort_values(by='geography')
    df = pd.DataFrame(df)
    df = df.drop(['geometry'],axis=1)
    df = df.set_index(['lat', 'lon','geography'], append='key').unstack()
    df.columns = df.columns.droplevel()
    values = {'Block_Group': 'N/A', 'Neighborhood_Long': 'N/A', 'Neighborhood_Short': 'N/A',
              'Seattle_City_Council_District': 'N/A', 'Urban_Village': 'N/A', 'Zipcode': 'N/A'}
    df = df.fillna(value=values)
    
    return (df)

def main(argv):
    input_file = str(sys.argv[1]) + '.csv' # add directory where the file should be found
    output_file = str(sys.argv[2]) + '.csv'
    pickle_name = str(sys.argv[3])
    reference = gi.get_reference(DATADIR, PROCESSED_DIR, pickle_name)
    decoded = geocode(input_file, reference)
    # print(decoded)

    decoded.to_csv(PROCESSED_DIR + output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
