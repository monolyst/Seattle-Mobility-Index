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
import altair as alt
import pandas as pd
import geopandas as gpd
import json
import constants as cn
import shapely.wkt
import data_accessor as daq
from coordinate import Coordinate

colors = 9
cmap = 'Blues'
figsize = (16, 10)

class GeoViz(object):
    def __init__(self):
        pass

    def get_blockgroup_geometries(self):
        """
        Loads SeattleCensusBlockGroups geometries as geodataframe from pickle file.
        Inputs: pickle
        Outputs: geodataframe, pickle if it does not exist
        """
        try:
            daq.open_pickle(cn.PICKLE_DIR, cn.SEATTLE_BLOCK_GROUPS_PICKLE)
        except FileNotFoundError:
            df = pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP, dtype={cn.KEY: str}).loc[:, (cn.KEY, cn.GEOMETRY, cn.LAT, cn.LON)]
            df[cn.COORDINATE] = df.apply(lambda x: Coordinate(x.lat, x.lon).set_geocode(), axis=1)
            df[cn.NBHD_SHORT] = df[cn.COORDINATE].apply(lambda x: x.neighborhood_short)
            df[cn.NBHD_LONG] = df[cn.COORDINATE].apply(lambda x: x.neighborhood_long)
            df[cn.COUNCIL_DISTRICT] = df[cn.COORDINATE].apply(lambda x: x.council_district)
            df[cn.URBAN_VILLAGE] = df[cn.COORDINATE].apply(lambda x: x.urban_village)
            df[cn.ZIPCODE] = df[cn.COORDINATE].apply(lambda x: x.zipcode)
            df.drop(columns = [cn.COORDINATE, cn.LAT, cn.LON], inplace=True)
            df.geometry = df.geometry.apply(shapely.wkt.loads)
            gdf = gpd.GeoDataFrame(df, crs=cn.CRS_EPSG, geometry=cn.GEOMETRY)
            daq.make_pickle(cn.PICKLE_DIR, gdf, cn.SEATTLE_BLOCK_GROUPS_PICKLE)
            return gdf
        else:
            return daq.open_pickle(cn.PICKLE_DIR, cn.SEATTLE_BLOCK_GROUPS_PICKLE)


    def load_choropleth_attribute(self, file_name, processed_dir=cn.CSV_DIR):
        """
        Loads data for choropleth into dataframe from csv file.
        Inputs: csv file name for data desired to be choropleth
        Outputs: dataframe
        """
        df = pd.read_csv(os.path.join(processed_dir, file_name), dtype={cn.KEY: str})
        df.key = df.key.apply(lambda x: x.rstrip('.0'))
        return df


    def merge_data(self, df=None, file_name=None, processed_dir=cn.CSV_DIR):
        """
        Merges geometry geodataframe with chloropleth attribute data.
        Inputs: dataframe or csv file name for data desired to be choropleth
        Outputs: dataframe
        """
        block_groups = self.get_blockgroup_geometries()
        if df is not None:
            attribute = df
        else:
            attribute = self.load_choropleth_attribute(file_name, processed_dir)
        
        return block_groups.merge(attribute, on=cn.KEY, how='inner')
        

    def plot_map(self, attribute_column, df=None, file_name=None, processed_dir=cn.CSV_DIR):
        """
        Plots geodataframe using the attribute as the chloropleth
        Inputs: column to be plotted as chloropleth, filename of csv file (optional)
        Outputs: plot
        """
        df = self.merge_data(df, file_name, processed_dir)
        gdf = gpd.GeoDataFrame(df, crs=cn.CRS_EPSG, geometry=cn.GEOMETRY)
        gdf.plot(column=attribute_column, cmap=cmap, figsize=figsize, scheme='equal_interval',
            k=colors, categorical=True, legend=True)
        
    def prepare_for_altair(self, df=None, file_name=None, processed_dir=cn.CSV_DIR):
        df = self.merge_data(df, file_name, processed_dir)
        gdf = gpd.GeoDataFrame(df, crs=cn.CRS_EPSG, geometry=cn.GEOMETRY)
        json_gdf = gdf.to_json()
        json_features = json.loads(json_gdf)
        return alt.Data(values=json_features['features'])

class ModeChoiceGeoViz(GeoViz):
    def __init__(self):
        pass

    def plot_map_altair(self, df=None, file_name=None, processed_dir=cn.CSV_DIR):
        data_geo = self.prepare_for_altair(df, file_name, processed_dir)
        multi = alt.selection_multi()
        return alt.Chart(data_geo).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).properties(
            projection={'type': 'mercator'},
            width=300,
            height=600,
            selection=multi
        ).encode(
            color=alt.condition(multi, 'properties.mode_index_scaled:Q', alt.value('lightgray')),
            tooltip=('properties.key:Q', 'properties.neighborhood_short:N',
                     'properties.neighborhood_long:N', 'properties.seattle_city_council_district:N',
                     'properties.urban_village:N', 'properties.zipcode:N', 'properties.mode_index:Q',
                     'properties.driving:Q', 'properties.transit:Q', 
                     'properties.bicycling:Q', 'properties.walking:Q')
        )


class AffordabilityGeoViz(GeoViz):
    def __init__(self):
        pass

    def plot_map_altair(self, df=None, file_name=None, processed_dir=cn.CSV_DIR):
        data_geo = self.prepare_for_altair(df, file_name, processed_dir)
        multi = alt.selection_multi()
        return alt.Chart(data_geo).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).properties(
            projection={'type': 'mercator'},
            width=300,
            height=600,
            selection=multi
        ).encode(
            color=alt.condition(multi, 'properties.scaled:Q', alt.value('lightgray')),
            tooltip=('properties.key:Q', 'properties.neighborhood_short:N',
                     'properties.neighborhood_long:N', 'properties.seattle_city_council_district:N',
                     'properties.urban_village:N', 'properties.zipcode:N', 'properties.cost:Q',
                     'properties.adjusted_for_income:Q', 'properties.normalized:Q', 'properties.scaled:Q')
        )
