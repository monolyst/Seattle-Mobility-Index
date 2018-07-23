import init
import constants as cn
import pandas as pd
import geopandas as gpd
import sqlite3
import support.trip as tp

class IndexBase(object):
    DATADIR = cn.CSV_DIR

    def __init__(self, time_of_day, type_of_day, travel_mode,
        db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR):
        self.time_of_day = time_of_day
        self.type_of_day = type_of_day
        self.travel_mode = travel_mode
        self.datadir = datadir
        self.trip_data = self.get_sql_data(db_name)
        self.score = None


    def get_csv_data(self, filename, datadir=DATADIR):
        df = pd.read_csv(str(filename) + '.csv')
        return df

    def get_sql_data(self, filename, datadir=DATADIR):
        df = daq.sql_to_df()
        return df

    def define_trip(self, travel_cost, mode, row):
        origin = self.trip_data.loc[row, cn.ORIGIN]
        destination = self.trip_data.loc[row, cn.DESTINATION]
        distance = self.trip_data.loc[row, cn.DISTANCE]
        duration = self.trip_data.loc[row, cn.DURATION]
        basket_category = self.trip_data.loc[row, cn.CLASS]
        pair = self.trip_data.loc[row, cn.PAIR]
        departure_time = self.trip_data.loc[row, cn.DEPARTURE_TIME]
        rank = self.trip_data.loc[row, cn.RANK]

        if mode == cn.CAR:
            duration_in_traffic = self.trip_data.loc[row, cn.DURATION_IN_TRAFFIC]
            trip = tp.CarTrip(origin, destination, distance, duration, basket_category,
                pair, departure_time, rank, duration_in_traffic)
        elif mode == cn.TRANSIT:
            fare_value = self.trip_data.loc[row, cn.FARE_VALUE]
            trip = tp.TranistTrip(origin, destination, distance, duration, basket_category,
                pair, departure_time, rank, fare_value)
        elif mode == cn.BIKE:
            trip = tp.BikeTrip(origin, destination, distance, duration, basket_category,
                pair, departure_time, rank)
        elif mode == cn.WALK:
            trip = tp.WalkTrip(origin, destination, distance, duration, basket_category,
                pair, departure_time, rank)
        return trip


    def calculate_score(self):
        trips = [] # will be a list of trip objects
        # for row in range(len(viable_modes)):
        #     # this syntax functions like a switch-case statement in java,
        #     # see: https://simonwillison.net/2004/May/7/switch/
        #     mode = {0: lambda row: cn.CAR,
        #             1: lambda row: cn.TRANSIT,
        #             2: lambda row: cn.BIKE,
        #             3: lambda row: cn.WALK}[row % 4](row)
        #     if viable_modes[row] == 1:
        #         trips.append(self.define_trip(mode, row))
        # this is how I am getting a list of trip objects for affordability index


