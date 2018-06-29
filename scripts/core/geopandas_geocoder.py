import os
import sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geocoder_input as gi

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')
PROCESSED_DIR = os.path.join(os.getcwd(), '../../seamo/data/processed/')

#Geocoder function
def geocode(lat, long):
    lat_long = gpd.GeoDataFrame([Point(long, lat)], columns=['geometry'], geometry='geometry')
    lat_long.crs = {'init' :'epsg:4326'}

    df = gpd.sjoin(lat_long, reference, how='inner')
    df = df.drop(columns='index_right')
    df = df.sort_values(by='Index')
    df.loc[-2] = lat
    df.loc[-1] = long
    df.sort_index(inplace=True)
    labels = pd.DataFrame(columns=['Latitude', 'Longitude', 'Block Group', 'Neighborhood_short', 'Neighborhood_long', 'Zip Code', 'Council District', 'UrbanVillage'])
    labels.loc[1] = df['keys'].tolist()

    return labels

def main(argv):
    reference = gi.make_dataframe(DATADIR)
    df = pd.read_csv(sys.argv[1])
    decoded = decoded.append(geocode(df['lat'], df['long']), axis=1)

    print(decoded)

    decoded.to_csv(PROCESSED_DIR)


if __name__ == "__main__":
    main(sys.argv[1:])
