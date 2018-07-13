import init
import index_base_class
import constants as cn

class AffordabilityIndex(index_base_class):
    DATADIR = cn.CSV_DIR

    def __init__(self, time_of_day, type_of_day, travel_mode, travel_cost,
        db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR):
        self.time_of_day = time_of_day
        self.type_of_day = type_of_day
        self.travel_mode = travel_mode
        self.travel_cost = travel_cost
        self.datadir = datadir
        self.trip_data = query_trip_data(db_name)
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

    def calculate_score(self, travel_cost):
        pass


