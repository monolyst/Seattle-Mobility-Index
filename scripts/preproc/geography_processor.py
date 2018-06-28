import os
import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from geopandas.tools import sjoin
# import matplotlib.pyplot as plt


# plt.rcParams["figure.figsize"] = [16, 9] #optional
def read_file_into_dataframe(desired_geometry, name, crs):
    # shapefile filepath
    desired_geometry = str(desired_geometry) + '.shp'
    FP = os.path.join(os.pardir, os.pardir,
        'seamo/data/raw/shapefiles/', desired_geometry)

    # read filepath into dataframe
    df = gpd.read_file(FP)

    # convert stateplane to lat/long
    df = df.to_crs({'init': 'epsg:4326'})

    # select desired columns and convert into geodataframe
    gdf = gpd.GeoDataFrame(df.loc[:, (name, 'geometry')],
        crs=crs, geometry='geometry')
    return gdf


def process_data(desired_geometry, name, crs, outline, rectangle):
    gdf = read_file_into_dataframe(desired_geometry, name, crs)
    seattle = gpd.overlay(outline, rectangle, how='intersection')
    seattle.crs = from_epsg(4326)
    seattle.crs = gdf.crs

    # spatial join between king county and seattle
    data = sjoin(gdf, seattle, op='intersects')

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
    outline.columns = ['geometry']
    return outline


def write_to_csv(desired_output, data):
    desired_output = str(desired_output) + '.csv'
    PRCOESSED_FP = os.path.join(os.pardir, os.pardir,
        'seamo/data/processed/csv_files/', desired_output)
    data.to_csv(PRCOESSED_FP)


def main():
    # create boundary for seattle
    crs = {'init': 'epsg:4326'}
    rectangle = gpd.GeoDataFrame([Polygon([(-122.435896, 47.734000),
        (-122.285766, 47.734000),
        (-122.285766, 47.735004),
        (-122.246627, 47.683255),
        (-122.245314, 47.495860),
        (-122.435896, 47.495860)])],
        columns=['geometry'], geometry='geometry')
    rectangle.crs = from_epsg(4326)

    # Block Group
    # shape file and correlation csv filepaths
    SEATTLE_FP = 'seamo/data/raw/SeattleCensusBlocksandNeighborhoodCorrelationFile.xlsx'
    SEATTLE_FP = os.path.join(os.pardir, os.pardir, SEATTLE_FP)

    # read filepath into dataframe
    seattle_data = pd.read_excel(SEATTLE_FP)

    # select desired columns
    s_data = seattle_data.loc[:, 'GEOID10'].astype(str).str[6:12].unique()

    # process Seattle correlation dataframe
    s = pd.DataFrame(s_data.astype(str))
    s.columns = ['tract_blkgrp']

    # process King County correlation dataframe
    gdf = read_file_into_dataframe('blkgrp10_shore', 'GEO_ID_GRP', crs)
    tract_blkgrp = gdf.loc[:, 'GEO_ID_GRP'].str[6:].astype(str)
    geometry = gdf.loc[:, 'geometry']
    tract_blkgrp.to_frame(name='tract_blkgrp')
    geometry.to_frame(name='geometry')
    kc = pd.concat([tract_blkgrp, geometry], axis=1)
    kc.columns = ['tract_blkgrp', 'geometry']

    # inner join on Seattle census tract/block groups
    kc_s_join = pd.merge(s, kc, left_on='tract_blkgrp',
        right_on='tract_blkgrp', how='inner')

    # convert pandas dataframe to geopandas dataframe
    gdf = gpd.GeoDataFrame(kc_s_join, crs=crs, geometry='geometry')
    gdf.crs = from_epsg(4326)

    # rectangle.crs = gdf.crs

    # overlay boundary of seattle with current outline to remove noise
    data = gpd.overlay(gdf, rectangle, how='intersection')

    # plot map
    # seattle.plot(cmap="tab20b")

    # calculate centroids
    blkgrps = pd.concat([data, data.geometry.centroid], axis=1)
    blkgrps.columns = ['tract_blkgrp', 'geometry', 'centroid']

    # outline of seattle used for overlay intersection
    outline = seattle_outline(blkgrps, crs)

    # Neighborhood
    neighborhoods = process_data('neighborhood', 'NEIGHBORHO',
        crs, outline, rectangle)

    # Council District
    coucil_districts = process_data('sccdst', 'NAME',
        crs, outline, rectangle)

    # Zipcode
    zipcodes = process_data('zipcode', 'ZIPCODE',
        crs, outline, rectangle)

    # Urban Village
    urban_villages = process_data('DPD_uvmfg_polygon', 'UV_NAME',
        crs, outline, rectangle)

    # write to csv file
    write_to_csv('SeattleNeighborhoods', neighborhoods)
    write_to_csv('SeattleCouncilDistricts', coucil_districts)
    write_to_csv('SeattleZipcodes', zipcodes)
    write_to_csv('SeattleUrbanVillages', urban_villages)
    write_to_csv('SeattleCensusBlockGroups', blkgrps)


if __name__ == "__main__":
    main()
