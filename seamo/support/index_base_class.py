import init
import constants as cn
import pandas as pd
import geopandas as gpd
import trip
import data_accessor as daq

class IndexBase(object):
    DATADIR = cn.CSV_DIR

    def __init__(self):


    def get_csv_data(self, filename, datadir=DATADIR):
        df = pd.read_csv(str(filename) + '.csv')
        return df

    def get_sql_data(self, filename, datadir=DATADIR):
        df = daq.sql_to_df()
        return df

    def _define_trip(self, mode, origin, destination, distance, duration, basket_category,
                    departure_time, duration_in_traffic=None, fare_value=None):
        trip = {cn.DRIVING_MODE: trip.CarTrip(origin, destination, distance, duration,
                                              basket_category, departure_time,
                                              duration_in_traffic),
        cn.TRANSIT_MODE: trip.TransitTrip(origin, destination, distance, duration,
                                          basket_category, departure_time, fare_value),
        cn.BIKING_MODE: trip.BikeTrip(origin, destination, distance, duration,
                                      basket_category, departure_time),
        cn.WALKING_MODE: trip.WalkTrip(origin, destination, distance, duration,
                                       basket_category, departure_time)}[mode]


    def write_to_csv(self, df, output_file, processed_dir=cn.CSV_DIR):
        """
        Call data accessor module to write dataframe to csv.
        """
        daq.write_to_csv(df, output_file, processed_dir)


