import init
import constants as cn
import pandas as pd
import geopandas as gpd
import sqlite3

class IndexBase(object):
    DATADIR = cn.CSV_DIR

    def __init__(self, time_of_day, type_of_day, travel_mode,
        db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR):
        self.time_of_day = time_of_day
        self.type_of_day = type_of_day
        self.travel_mode = travel_mode
        self.datadir = datadir
        self.trip_data = self.query_trip_data(db_name)
        self.score = None


    def query_trip_data(self, db_name=cn.GOOGLE_DIST_MATRIX_OUT):
        db_file = os.path.join(cn.DB_DIR, db_name + '.db')
        conn = sqlite3.connect(db_file)
        df = read_sql_table(db_file, conn)
        conn.commit()
        conn.close()
        return df


    def get_data(self, filename, datadir=DATADIR):
        df = pd.read_csv(str(filename) + '.csv')
        return df

    def calculate_score(self):
        pass


