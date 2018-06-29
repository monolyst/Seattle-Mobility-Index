import os

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

blkgrp = gpd.read_file(os.path.join(DATADIR, "blkgrp10_shore.shp"))
blkgrp = blkgrp.loc[:, ('GEO_ID_GRP', 'geometry')]
blkgrp = blkgrp.to_crs({'init' :'epsg:4326'})
blkgrp.rename(columns={blkgrp.columns[0]: 'keys'}, inplace=True)
blkgrp['Index'] = int(1)

nbhd = gpd.read_file(os.path.join(DATADIR, "Neighborhoods.shp"))
nbhd_short = nbhd.loc[:, ('S_HOOD', 'geometry')]
nbhd_long = nbhd.loc[:, ('L_HOOD', 'geometry')]
nbhd_short.rename(columns={nbhd_short.columns[0]: 'keys'}, inplace=True)
nbhd_long.rename(columns={nbhd_long.columns[0]: 'keys'}, inplace=True)
nbhd_short['Index'] = int(2)
nbhd_long['Index'] = int(3)

zipcode = gpd.read_file(os.path.join(DATADIR, "zipcode.shp"))
zipcode = zipcode.loc[:, ('ZIPCODE', 'geometry')]
zipcode = zipcode.to_crs({'init' :'epsg:4326'})
zipcode.rename(columns={zipcode.columns[0]: 'keys'}, inplace=True)
zipcode['Index'] = int(4)

scc = gpd.read_file(os.path.join(DATADIR, "sccdst.shp"))
scc = scc.loc[:, ('SCCDST', 'geometry')]
scc = scc.to_crs({'init' :'epsg:4326'})
scc.rename(columns={scc.columns[0]: 'keys'}, inplace=True)
scc['Index'] = int(5)

urbanvillage = gpd.read_file(os.path.join(DATADIR, "DPD_uvmfg_polygon.shp"))
urbanvillage = urbanvillage.loc[:, ('UV_NAME', 'geometry')]
urbanvillage.rename(columns={urbanvillage.columns[0]: 'keys'}, inplace=True)
urbanvillage['Index'] = int(6)

#Concatenate all GeoDataFrames into a single data
reference = pd.concat([blkgrp, nbhd_short, nbhd_long, zipcode, scc, urbanvillage])

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


print(geocode(47.650955, -122.34728))
