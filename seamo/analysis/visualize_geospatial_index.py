"""
Module for plotting geospatial chloropleth maps.
Data passed should have the blockgroups column labeled 'key'.
Inputs: either dataframe or csv file
Outputs: geospatial chloropleth plot

To use with dataframe:
$ plot_map('column_name', df='df_name')

To use with csv file:
$ plot_map('column_name', file_name='file_name')
"""

import init
import os
import pandas as pd
import geopandas as gpd
import constants as cn
import shapely.wkt
import data_accessor as daq

colors = 9
cmap = 'Blues'
figsize = (16, 10)

def get_blockgroup_geometries():
    """
    Loads SeattleCensusBlockGroups geometries as geodataframe from pickle file.
    Inputs: pickle
    Outputs: geodataframe, pickle if it does not exist
    """
    try:
        daq.open_pickle(cn.PICKLE_DIR, cn.SEATTLE_BLOCK_GROUPS_PICKLE)
    except:
        df = pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP, dtype={cn.KEY: str}).loc[:, (cn.KEY, cn.GEOMETRY)]
        df.geometry = df.geometry.apply(shapely.wkt.loads)
        gdf = gpd.GeoDataFrame(df, crs=cn.CRS_EPSG, geometry=cn.GEOMETRY)
        daq.make_pickle(cn.PICKLE_DIR, gdf, cn.SEATTLE_BLOCK_GROUPS_PICKLE)
        return gdf
    else:
        return daq.open_pickle(cn.PICKLE_DIR, cn.SEATTLE_BLOCK_GROUPS_PICKLE)


def load_choropleth_attribute(file_name, processed_dir=cn.CSV_DIR):
    """
    Loads data for choropleth into dataframe from csv file.
    Inputs: csv file name for data desired to be choropleth
    Outputs: dataframe
    """
    df = pd.read_csv(os.path.join(processed_dir, file_name), dtype={cn.KEY: str})
    df.key = df.key.apply(lambda x: x.rstrip('.0'))
    return df


def merge_data(df=None, file_name=None, processed_dir=cn.CSV_DIR):
    """
    Merges geometry geodataframe with chloropleth attribute data.
    Inputs: dataframe or csv file name for data desired to be choropleth
    Outputs: dataframe
    """
    block_groups = get_blockgroup_geometries()
    if df == None:
        attribute = load_choropleth_attribute(file_name, processed_dir)
    else:
        attribute = df
    return block_groups.merge(attribute, on=cn.KEY, how='inner')
    

def plot_map(attribute_column, df=None, file_name=None, processed_dir=cn.CSV_DIR):
    """
    Plots geodataframe using the attribute as the chloropleth
    Inputs: column to be plotted as chloropleth, filename of csv file (optional)
    Outputs: plot
    """
    df = merge_data(df, file_name, processed_dir)
    gdf = gpd.GeoDataFrame(df, crs=cn.CRS_EPSG, geometry=cn.GEOMETRY)
    gdf.plot(column=attribute_column, cmap=cmap, figsize=figsize, scheme='equal_interval',
        k=colors, categorical=True, legend=True)