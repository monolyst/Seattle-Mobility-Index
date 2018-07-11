import __init__
import constants as cn
import pandas as pd
import geopandas as gpd
import sqlite3

class IndexBaseClass(object):
    DATADIR = cn.CSV_DIR

    def __init__(self, day_type, time_span, travel_mode):
        self.day_type = day_type
        self.time_span = time_span
        self.travel_mode = travel_mode
        self.trip_data = query_trip_data()


    def query_trip_data():
        db_file = os.path.join(cn.DB_DIR, cn.GOOGLE_DIST_MATRIX_OUT + '.db')
        conn = sqlite3.connect(db_file)
        df = read_sql_table(cn.GOOGLE_DIST_MATRIX_OUT, conn)
        conn.commit()
        conn.close()
        return df


    def get_data(filename, datadir=DATADIR):
