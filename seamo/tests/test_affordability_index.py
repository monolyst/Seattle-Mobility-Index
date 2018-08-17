"""
This is a test file for trip.py
"""
import init
import unittest
from affordability_index import AffordabilityIndex
from trip import CarTrip
import pandas as pd
import constants as cn
import numpy as np

origin1 = '530330094004'
origin2 = '530330094004'
dest_lat = 47.6145
dest_lon = -122.3210
duration = 32.183333
distance = 16.040398
duration_in_traffic = 3.303167
basket_category = 'citywide'
departure_time = '2018-06-06 12:41:31.092964'
car1 = CarTrip(origin1, dest_lat, dest_lon, distance, duration, basket_category, departure_time, duration_in_traffic)
car2 = CarTrip(origin2, dest_lat, dest_lon, distance, duration, basket_category, departure_time, duration_in_traffic)

TEST = {origin1: [car1, car2], origin2: [car1, car2]}

class AffordabilityIndexTest(unittest.TestCase):
    def setUp(self):
        self.a_index = AffordabilityIndex(TEST)

    def test_create_avg_blockgroup_cost_df(self):
        result_df = self.a_index.create_avg_blockgroup_cost_df()
        test_df = pd.DataFrame({cn.KEY: ['530330094004', '530330094004'], cn.COST: [21.465577, 21.465577]})
        import pdb; pdb.set_trace()
        self.assertTrue(np.isclose(test_df[cn.COST], result_df[cn.COST], atol=1e-03))

    def test_calculate_score(self):
        pass

    
suite = unittest.TestLoader().loadTestsFromTestCase(AffordabilityIndexTest)
_ = unittest.TextTestRunner().run(suite)