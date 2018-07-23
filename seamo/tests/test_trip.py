"""
This is a test file for trip.py
"""
import init
import unittest
import trip
import coordinate
import constants as cn

SEATTLE_ORIGIN = (47.6145, -122.3210)
SEATTLE_DESTINATION = (47.6145, -122.3210)

NONSEATTLE_ORIGIN = (-122.3210, 47.6145)
NONSEATTLE_DESTINATION = (-122.3210, 47.6145)

DURATION = 32.183333
DISTANCE = 16.040398
DURATION_IN_TRAFFIC = 3.303167
BASKET_CATEGORY = cn.CITYWIDE
PAIR = '530330006001-Overlake-Redmond'
DEPARTURE_TIME = '2018-06-06 12:41:31.092964'
RANK = 14.0
BASE_COST = DURATION * cn.VOT_RATE / cn.MIN_TO_HR
PARKING_COST = 3.0

class TripTest(unittest.TestCase):
    def setUp(self):
        self.trip = trip.Trip(SEATTLE_ORIGIN, SEATTLE_DESTINATION, 'mode', DISTANCE, DURATION,
            BASKET_CATEGORY, PAIR, DEPARTURE_TIME, RANK)

    def test_convert_to_coord(self):
        EXPECTED_LAT = 47.6145
        EXPECTED_LON = -122.3210
        EXPECTED_COORD = str(EXPECTED_LAT) + ', ' + str(EXPECTED_LON)

        self.assertEquals(EXPECTED_COORD, str(self.trip._convert_to_coord((47.6145, -122.3210))))

    def test_set_persona(self):
        pass

    def test_calculate_base_cost(self):
        self.assertEquals(BASE_COST, self.trip._calculate_base_cost(DURATION))

    def test_get_place(self):
        pass

    def test_get_trip_id(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TripTest)
_ = unittest.TextTestRunner().run(suite)


class CarTripTest(unittest.TestCase):
    def setUp(self):
        MODE = cn.CAR
        import pdb; pdb.set_trace()
        self.car_trip = trip.CarTrip(SEATTLE_ORIGIN, SEATTLE_DESTINATION, MODE, DISTANCE, DURATION,
            BASKET_CATEGORY, PAIR, DEPARTURE_TIME, RANK, DURATION_IN_TRAFFIC)

    def test_calculate_car_duration(self):
        EXPECTED_DURATION = DURATION + DURATION_IN_TRAFFIC
        self.assertEquals(EXPECTED_DURATION, self.car_trip(DURATION, DURATION_IN_TRAFFIC))

    def test_calculate_cost(self):
        COST = BASE_COST + (DISTANCE * cn.AAA_RATE) + PARKING_COST
        self.assertEquals(COST, self.car_trip._calculate_cost(SEATTLE_DESTINATION, DURATION,
            DEPARTURE_TIME, cn.AAA_RATE, cn.VOT_RATE))
        

    def test_get_time_data(self):
        TEST_LIST = ['weekday_morning_', 'weekday_afternoon_', 'weekday_evening_',
        'weekend_morning_', 'weekend_afternoon_', 'weekend_evening_']
        TEST_DURATION = 1.5

        TIMESTAMPS = ['2018-06-04 9:41:31.092964', '2018-06-06 12:41:31.092964',
                    '2018-06-08 19:41:31.092964', '2018-06-09 9:41:31.092964',
                    '2018-06-10 12:41:31.092964', '2018-06-17 19:41:31.092964']

        for i in range(len(TIMESTAMPS)):
            self.assertEquals(TEST_LIST[i], self.car_trip._get_time_date(TEST_DURATION, TIMESTAMPS[i]))


suite = unittest.TestLoader().loadTestsFromTestCase(CarTripTest)
_ = unittest.TextTestRunner().run(suite)