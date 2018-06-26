import os
import pandas as pd
import geopandas as gpd
import pdb
# import matplotlib.pyplot as plt


# plt.rcParams["figure.figsize"] = [16, 9] #optional

def main():
    #shape file and correlation csv filepaths
    KING_COUNTY_FP = 'seamo/data/raw/blkgrp10_shore/blkgrp10_shore.shp'
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
    coordinates = kc_data.loc[:, 'geometry']
    tract_blkgrp.to_frame(name='tract_blkgrp')
    coordinates.to_frame(name='coordinates')
    kc = pd.concat([tract_blkgrp, coordinates],axis=1)
    kc.columns=['tract_blkgrp', 'coordinates']

    #inner join on Seattle census tract/block groups
    kc_s_join = pd.merge(s, kc, left_on='tract_blkgrp',
        right_on='tract_blkgrp', how='inner')

    #convert pandas dataframe to geopandas dataframe
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(kc_s_join, crs=crs, geometry='coordinates')

    #plot map
    # gdf.plot(cmap="tab20b")

    #calculate centroids
    data = pd.concat([gdf, gdf.coordinates.centroid], axis=1)
    data.columns=['tract_blkgrp', 'coordinates', 'centroid']

    #write to csv file
    PRCOESSED_DATA_FP = 'seamo/data/processed/SeattleCensusBlockGroups.csv'
    fp = king_county = os.path.join(os.pardir, PRCOESSED_DATA_FP)
    data.to_csv(fp)

if __name__ == "__main__":
    main()