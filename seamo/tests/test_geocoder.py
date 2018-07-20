"""
This is a test file for universal_geocoder.py
"""
import __init__
import geocoder
import constants
import unittest
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



suite = unittest.TestLoader().loadTestsFromTestCase(UniGeoTest)
_ = unittest.TextTestRunner().run(suite)