import unittest
import pandas as pd

import init
import constants as cn
from basket_calculator import *


class BasketCalcTest(unittest.TestCase):

    def setUp(self):
        """
        Set up Basket Calculator test with origin and destination dataframes
        each containing three rows of sample data.
        """
        origin_data = { cn.BLOCKGROUP: [1, 2, 3],
                        cn.CENSUS_LAT: [47.72683, 47.51008, 47.68651],
                        cn.CENSUS_LON: [-122.28469, -122.38054, -122.30147] } 
        self.origin_df = pd.DataFrame.from_dict(origin_data)

        dest_data = { cn.GOOGLE_PLACES_LAT: [47.6158665, 47.6183442, 47.6229294],
                      cn.GOOGLE_PLACES_LON: [-122.3099133, -122.3380965, -122.3223185],
                      cn.CLASS: ['supermarket', 'supermarket', 'library'],
                      cn.PLACE_ID: ['trader_joes', 'whole_foods', 'cap_library'] }
        self.dest_df = pd.DataFrame.from_dict(dest_data)


    def test_create_dist_df(self):
        """
        Create a DataFrame with distances from all origins to all destinations
        (No threshold)
        """
        dist_df = origins_to_destinations(self.origin_df, self.dest_df,
                                          'haversine', False)
        self.assertIsInstance(dist_df, pd.DataFrame) 
        size = len(self.origin_df) * len(self.dest_df)
        self.assertEqual(size, len(dist_df))

    def test_basket_rank(self):
        # Check columns
        # Check ranks are integers
        # Check size of input and output match
        pass


    def test_create_basket(self):
        # Check that each blockgroup has a basket of 25 
        # Check that the count for each category matches basket
        # Check that every pair is unique
        pass

if __name__ == "__main__":
    unittest.main()

