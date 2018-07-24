import init
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import pickle
import constants as cn
import geocode_input_base_class as gib

# Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')
class ParkingCostInput(gib.GeocodeInputBase):
    def __init__(self):
        super().__init__()

    def read_shapefile(self, raw_dir, shapefile, council_district):
        gdf = super().read_shapefile(raw_dir, shapefile)
        for col in gdf:
            # get dtype for column
            col_type = gdf[col].dtype 
            # check if it is a number
            if col_type == int or col_type == float:
                gdf[col].fillna(0, inplace=True)
            else:
                gdf[col].fillna('None', inplace=True)
        gdf = gdf.loc[:, cn.PARKING_COLUMNS]
        gdf = gdf[gdf[cn.PRIMARY_DISTRICT] == council_district]
        gdf = gdf.drop(columns = [cn.PRIMARY_DISTRICT])
        gdf.columns = [cn.BLOCK_FACE, cn.PARKING_CATEGORY, cn.WEEKDAY_MORNING_RATE,
            cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE, cn.WEEKDAY_MORNING_START,
            cn.WEEKDAY_MORNING_END, cn.WEEKDAY_AFTERNOON_START, cn.WEEKDAY_AFTERNOON_END,
            cn.WEEKDAY_EVENING_START, cn.WEEKDAY_EVENING_END, cn.WEEKEND_MORNING_RATE,
            cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE, cn.WEEKEND_MORNING_START,
            cn.WEEKEND_MORNING_END, cn.WEEKEND_AFTERNOON_START, cn.WEEKEND_AFTERNOON_END,
            cn.WEEKEND_EVENING_START, cn.WEEKEND_EVENING_END, cn.GEOMETRY]
        gdf.drop(gdf[gdf.geometry == 'None'].index, inplace=True)
        gdf.crs = cn.CRS_EPSG
        return gdf


    def make_reference(self, raw_dir, processed_dir, pickle_name):
        council_district = {cn.DISTRICT1_PICKLE: cn.DISTRICT1,
                    cn.DISTRICT2_PICKLE: cn.DISTRICT2,
                    cn.DISTRICT3_PICKLE: cn.DISTRICT3,
                    cn.DISTRICT4_PICKLE: cn.DISTRICT4,
                    cn.DISTRICT5_PICKLE: cn.DISTRICT5,
                    cn.DISTRICT6_PICKLE: cn.DISTRICT6,
                    cn.DISTRICT7_PICKLE: cn.DISTRICT7}[pickle_name]
        parking = self.read_shapefile(raw_dir, cn.BLOCK_FACE_FNAME, council_district)        
        intervals = [cn.WEEKDAY_MORNING_START, cn.WEEKDAY_AFTERNOON_START, cn.WEEKDAY_EVENING_START,
            cn.WEEKDAY_MORNING_END, cn.WEEKDAY_AFTERNOON_END, cn.WEEKDAY_EVENING_END,
            cn.WEEKEND_MORNING_START, cn.WEEKEND_AFTERNOON_START, cn.WEEKEND_EVENING_START,
            cn.WEEKEND_MORNING_END, cn.WEEKEND_AFTERNOON_END,cn.WEEKEND_EVENING_END]
        for interval in intervals:
            parking[interval] = parking[interval].apply(lambda x:
                int(x / cn.MIN_TO_HR) if pd.notnull(x) else x)
            parking[interval] = parking[interval].apply(lambda x:
                x if x != 0 else np.nan)
        # Make a copy of the blockface geoDataFrame because buffer replaces the geometry column with the buffer polygons
        reference = parking.copy()
        # The distance value is in degrees beucase we are using epsg4326.
        reference.geometry = parking.geometry.buffer(cn.BUFFER_SIZE)

        self.make_pickle(processed_dir, reference, pickle_name)
        return reference