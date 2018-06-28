import os
import pandas as pd
import geopandas as gpd
import pdb
import sys
from fiona.crs import from_epsg
from shapely.geometry import Polygon
# import matplotlib.pyplot as plt


# plt.rcParams["figure.figsize"] = [16, 9] #optional

def main(file_type):
    #shape file and correlation csv filepaths
    KING_COUNTY_FP = 'seamo/data/raw/shapefiles/blkgrp10_shore.shp'
    SEATTLE_FP = 'seamo/data/raw/SeattleCensusBlocksandNeighborhoodCorrelationFile.xlsx'
    king_county = os.path.join(os.pardir, KING_COUNTY_FP)
    seattle = os.path.join(os.pardir, SEATTLE_FP)

    #read filepaths into dataframes
    
    # pdb.set_trace()
    king_county_data = gpd.read_file(king_county)
    seattle_data = pd.read_excel(seattle)

    #convert stateplane to lat/long
    king_county_data = king_county_data.to_crs({'init': 'epsg:4326'}) 

    #select desired columns
    kc_data = king_county_data.loc[:, ('GEO_ID_GRP','geometry')]
    s_data = seattle_data.loc[:, 'GEOID10'].astype(str).str[6:12].unique()

    #process Seattle correlation dataframe
    s = pd.DataFrame(s_data.astype(str))
    s.columns = ['tract_blkgrp']

    #process King County correlation dataframe
    tract_blkgrp = kc_data.loc[:, 'GEO_ID_GRP'].str[6:].astype(str)
    geometry = kc_data.loc[:, 'geometry']
    tract_blkgrp.to_frame(name='tract_blkgrp')
    geometry.to_frame(name='geometry')
    kc = pd.concat([tract_blkgrp, geometry],axis=1)
    kc.columns=['tract_blkgrp', 'geometry']

    #inner join on Seattle census tract/block groups
    kc_s_join = pd.merge(s, kc, left_on='tract_blkgrp',
        right_on='tract_blkgrp', how='inner')

    #convert pandas dataframe to geopandas dataframe
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(kc_s_join, crs=crs, geometry='geometry')
    gdf.crs = from_epsg(4326)

    #create boundary for seattle
    rectangle = gpd.GeoDataFrame([Polygon([(-122.435896, 47.734000),
        (-122.285766, 47.734000),
        (-122.285766, 47.735004),
        (-122.246627, 47.683255),
        (-122.245314, 47.495860),
        (-122.435896, 47.495860)])],
        columns=['geometry'], geometry='geometry')
    rectangle.crs = from_epsg(4326)
    rectangle.crs = gdf.crs

    #overlay boundary of seattle with current outline to remove noise
    seattle = gpd.overlay(gdf, rectangle, how='intersection')

    #plot map
    # seattle.plot(cmap="tab20b")

    #calculate centroids
    data = pd.concat([seattle, seattle.geometry.centroid], axis=1)
    data.columns=['tract_blkgrp', 'geometry', 'centroid']

    #write to csv file
    if file_type == 0:
        PRCOESSED_DATA_FP = 'seamo/data/processed/csv_files/SeattleCensusBlockGroups.csv'
        fp = king_county = os.path.join(os.pardir, PRCOESSED_DATA_FP)
        data.to_csv(fp)
    elif file_type == 1:
        PRCOESSED_DATA_FP = 'seamo/data/processed/json_files/SeattleCensusBlockGroups.geojson'
        fp = king_county = os.path.join(os.pardir, PRCOESSED_DATA_FP)
        data.to_file(fp, driver='GeoJSON')

if __name__ == "__main__":
    try:
        if sys.argv[1] == "csv":
            main(0)
        elif sys.argv[1] == "json":
            main(1)
    except:
        main(0)