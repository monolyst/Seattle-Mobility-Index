"""
This is a test file for universal_geocoder.py
"""
import init
import geocoder 
import constants as cn
import unittest
import pandas as pd
import os
#from scripts.core import geopandas_geocoder
# from .core import geopandas_geocoder
# import core.geopandas_geocoder as gg

class UniGeoTest(unittest.TestCase):
	def setUp(self):
		pass

	def test_get_reference(self):
		reference_gdf = geocoder.get_reference()
		EXPECTED_COLUMNS = ['key', 'geometry', 'geography']
		self.assertTrue(all(EXPECTED_COLUMNS == reference_gdf.columns))
		self.assertGreater(len(reference_gdf), 0)

	def test_geocode_csv_shape(self):
		EXPECTED_ROWS = 2
		EXPECTED_COLUMNS = 8
		DATA = os.path.join(cn.TEST_DIR, 'test.csv')
		test_data = geocoder.geocode_csv(DATA)
		self.assertTrue(test_data.shape[0] == EXPECTED_ROWS)
		self.assertTrue(test_data.shape[1] == EXPECTED_COLUMNS)

	def test_geocode_csv_blkgroup_classification_small(self):
		RANDOM_POINTS = os.path.join(cn.TEST_DIR, 'blkgrp_classification.csv')
		RANDOM_POINT_KEYS = os.path.join(cn.TEST_DIR, 'blkgrp_classification_key.csv')
		keys = pd.read_csv(RANDOM_POINT_KEYS)
		test_data = geocoder.geocode_csv(RANDOM_POINTS)
		self.assertTrue(all(test_data[cn.BLOCK_GROUP] == keys['key']))

		
	def test_geocode_csv_blkgroup_classification_LARGE(self):
		RANDOM_POINTS = os.path.join(cn.TEST_DIR, 'blkgrp_classification_LARGE.csv')
		RANDOM_POINT_KEYS = os.path.join(cn.TEST_DIR, 'blkgrp_classification_key_LARGE.csv')
		keys = pd.read_csv(RANDOM_POINT_KEYS)
		test_data = geocoder.geocode_csv(RANDOM_POINTS)
		self.assertTrue(all(test_data[cn.BLOCK_GROUP] == keys['key']))




suite = unittest.TestLoader().loadTestsFromTestCase(UniGeoTest)
_ = unittest.TextTestRunner().run(suite)