import init
import os
import sys
import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from geopandas.tools import sjoin
import spatial_overlays as sp
import constants as cn
# import matplotlib.pyplot as plt


# plt.rcParams["figure.figsize"] = [16, 9] #optional

def read_file_into_dataframe(desired_geometry, name, crs):
    # shapefile filepath
    desired_geometry = str(desired_geometry) + '.shp'
    FP = os.path.join(cn.SHAPEFILE_DIR, desired_geometry)

    # read filepath into dataframe
    df = gpd.read_file(FP)

    # convert stateplane to lat/long
    df = df.to_crs(cn.CRS_EPSG)

    # select desired columns and convert into geodataframe
    if desired_geometry == cn.BLKGRP_FNAME + '.shp':
        gdf = gpd.GeoDataFrame(df.loc[:, (name, cn.SHAPE_AREA, cn.GEOMETRY)],
            crs=crs, geometry=cn.GEOMETRY)

        # process columns from geodataframe
        tract_blkgrp = gdf.loc[:, cn.BLKGRP_KEY].str[6:].astype(str)
        geometry = gdf.loc[:, cn.GEOMETRY]
        area = gdf.loc[:, cn.SHAPE_AREA]

        # convert series back to dataframe
        tract_blkgrp.to_frame(name='tract_blkgrp')
        geometry.to_frame(name=cn.GEOMETRY)
        area.to_frame(name=cn.AREA)
        gdf = pd.concat([tract_blkgrp, geometry, area],axis=1)
        gdf.columns = ['tract_blkgrp', cn.GEOMETRY, cn.AREA]
    else:
        gdf = gpd.GeoDataFrame(df.loc[:, (name, cn.GEOMETRY)],
            crs=crs, geometry=cn.GEOMETRY)
        gdf.columns = [cn.KEY, cn.GEOMETRY]
    return gdf


def process_data(desired_geometry, name, crs, outline, rectangle):
    gdf = read_file_into_dataframe(desired_geometry, name, crs)
    seattle = sp.spatial_overlays(outline, rectangle, how='intersection')
    seattle = seattle.drop(['idx1', 'idx2'], axis=1)
    seattle.crs = from_epsg(4326)
    seattle.crs = gdf.crs

    # spatial join between king county and seattle
    data = sjoin(gdf, seattle, op='intersects')
    data = data[[cn.KEY, cn.GEOMETRY]]
    mask = data.key.duplicated(keep='first')
    data = data[~mask]

    # plot map
    # data.plot(cmap="tab20b")
    return data


def seattle_outline(df, crs):
    blkgrps = df.geometry
    polygons = blkgrps
    boundary = gpd.GeoSeries(cascaded_union(polygons))
    # boundary.plot(color = 'red')
    # plt.show()
    boundary.crs = from_epsg(4326)
    outline = gpd.GeoDataFrame(boundary, crs=crs)
    outline.columns = [cn.GEOMETRY]
    return outline


def write_to_csv(desired_output, data):
    PRCOESSED_FP = os.path.join(cn.CSV_DIR, str(desired_output) + '.csv')
    data.to_csv(PRCOESSED_FP)

def write_to_shapefile(desired_output, data):
    desired_output = os.path.join(cn.GEN_SHAPEFILE_DIR, str(desired_output) + '.shp')
    driver = 'ESRI Shapefile'
    data.to_file(desired_output, driver=driver)


def process():
    # create boundary for seattle
    crs = cn.CRS_EPSG
    rectangle = gpd.GeoDataFrame([Polygon([(-122.435896, 47.734000),
        (-122.285766, 47.734000),
        (-122.285766, 47.735004),
        (-122.246627, 47.683255),
        (-122.245314, 47.495860),
        (-122.435896, 47.495860)])],
        columns=[cn.GEOMETRY], geometry=cn.GEOMETRY)
    rectangle.crs = from_epsg(4326)

    # Block Group
    # shape file and correlation csv filepaths
    SEATTLE_FP = os.path.join(cn.RAW_DIR, 'SeattleCensusBlocksandNeighborhoodCorrelationFile.xlsx')

    # read filepath into dataframe
    seattle_data = pd.read_excel(SEATTLE_FP)

    # select desired columns
    s_data = seattle_data.loc[:, 'GEOID10'].astype(str).str[6:12].unique()

    # process Seattle correlation dataframe
    s = pd.DataFrame(s_data.astype(str))
    s.columns = ['tract_blkgrp']

    # process King County correlation dataframe
    gdf = read_file_into_dataframe(cn.BLKGRP_FNAME, cn.BLKGRP_KEY, crs)

    # inner join on Seattle census tract/block groups
    gdf = pd.merge(s, gdf, left_on='tract_blkgrp',
        right_on='tract_blkgrp', how='inner')

    # convert pandas dataframe to geopandas dataframe
    gdf = gpd.GeoDataFrame(gdf, crs=crs, geometry=cn.GEOMETRY)
    gdf.crs = from_epsg(4326)

    # overlay boundary of seattle with current outline to remove noise
    data = sp.spatial_overlays(gdf, rectangle, how='intersection')
    data = data[['tract_blkgrp', cn.AREA, cn.GEOMETRY]]

    # plot map
    # data.plot(cmap="tab20b")

    # calculate centroids
    centroids = data.geometry.centroid
    data['tract_blkgrp'] = '530330' + data['tract_blkgrp'].astype(str)
    blkgrps = pd.concat([data, centroids.y, centroids.x], axis=1)
    blkgrps.columns = [cn.KEY, cn.AREA, cn.GEOMETRY, cn.LAT, cn.LON]
    # print(blkgrps.head())

    # outline of seattle used for overlay intersection
    outline = seattle_outline(blkgrps, crs)

    # Short Neighborhood
    short_nbhd = process_data(cn.NBHD_FNAME, cn.NBHD_SHORT_KEY,
        crs, outline, rectangle)

    # Long Neighborhood
    long_nbhd = process_data(cn.NBHD_FNAME, cn.NBHD_LONG_KEY,
        crs, outline, rectangle)

    # Council District
    coucil_districts = process_data(cn.COUNCIL_DISTRICT_FNAME, cn.COUNCIL_DISTRICT_KEY,
        crs, outline, rectangle)

    # Zipcode
    zipcodes = process_data(cn.ZIPCODE_FNAME, cn.ZIPCODE_KEY,
        crs, outline, rectangle)

    # Urban Village
    urban_villages = process_data(cn.URBAN_VILLAGE_FNAME, cn.URBAN_VILLAGE_KEY,
        crs, outline, rectangle)

    return blkgrps, short_nbhd, long_nbhd, coucil_districts, zipcodes, urban_villages

def main(argv):
    try:
        sys.argv[1]
    except:
        raise "need an input"
    else:
        choice = str(sys.argv[1])
    blkgrps, short_nbhd, long_nbhd, coucil_districts, zipcodes, urban_villages = process()
    # write to csv file
    if '0' in choice:
        write_to_csv('SeattleShortNeighborhoods', short_nbhd)
    elif '1' in choice:
        write_to_csv('SeattleLongNeighborhoods', long_nbhd)
    elif '2' in choice:
        write_to_csv('SeattleCouncilDistricts', coucil_districts)
    elif '3' in choice:
        write_to_csv('SeattleZipcodes', zipcodes)
    elif '4' in choice:
        write_to_csv('SeattleUrbanVillages', urban_villages)
    elif '5' in choice:
        # print(blkgrps.head())
        write_to_csv('SeattleCensusBlockGroups', blkgrps)
        write_to_shapefile('SeattleCensusBlockGroups', blkgrps)


if __name__ == "__main__":
    main(sys.argv[1:])
