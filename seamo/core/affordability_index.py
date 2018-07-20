import init
import index_base_class
import constants as cn
import support.trip as tp

class AffordabilityIndex(index_base_class):
    DATADIR = cn.CSV_DIR

    def __init__(self, time_of_day, type_of_day, travel_mode,
        db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR, travel_cost):
        super().__init__(self, time_of_day, type_of_day, travel_mode,
            db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR)
        self.travel_cost = travel_cost


    def get_data(self, filename, datadir=DATADIR):
        df = pd.read_csv(str(filename) + '.csv')
        return df

    def define_trip(self, travel_cost, mode):
        if mode == 'car':
            car = tp.CarTrip(origin, destination, distance, duration, category,
                pair, departure_time, rank)
        elif mode == 'transit':
            transit = tp.TranistTrip(origin, destination, distance, duration, category,
                pair, departure_time, rank)
        elif mode == 'biking':
            bike = tp.BikeTrip(origin, destination, distance, duration, category,
                pair, departure_time, rank)
        elif mode == 'walking':
            walk = tp.WalkTrip(origin, destination, distance, duration, category,
                pair, departure_time, rank)

    def calculate_score(self):
        trip1 = self.define_trip()
        trip2 = self.define_trip()

        blkgrp_trip_cost = sum(trip1, trip2) / num_trips
        normalized = normalize(blkgrp_trip_cost)

        income_adjusted = blkgrp_trip_cost / income
        income_normalized = normalize(income_adjusted)

        return normalized, income_normalized

