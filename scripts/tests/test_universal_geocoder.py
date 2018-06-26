"""
This is a test file for universal_geocoder.py
"""

import unittest

class UniGeoTest(unittest.TestCase):

	def test_maxsize(self):
		"""
		foo
		"""

	def test_read_nshort(self):
		NUMBER_OF_VALUES = 1889
		NUMBER_OF_KEYS = 10
		key, value = csv.reader(open(os.path.join(data_path,
			"Neighborhoods-Short.csv")))

		self.assertEqual(NUMBER_OF_VALUES,)


		"""
		The purpose of this test is to ensure correct
		loading of the data from Neihborhoods-Short.csv
		"""
		
		
		#data type
		#dataframe dimensions

	def test_read_nlong(self):
		"""
		foo
		"""

	def test_read_sccdst(self):
		"""
		foo
		"""

	def test_read_zipcode(self):
		"""
		foo
		"""

	def test_read_urbvil(self):
		"""
		foo
		"""

	def test_read_blkgrp(self):
		"""
		foo
		"""
		

	def test_path_nshort(self):
		"""
		Ensure a path object was created for the Neighborhood-Short 
		geography.

		"""

	def test_contains_point(self):
		"""
		Given any polygon and point that is known to be in the polygon
		the geocoder correctly recognizes that the point is contained in the polygon.

		"""
	def test_correct_key(self):
		"""
		Given a sample of points with known classification within the geographies,
		the geocoder correctly identifies the key for each geography.
		"""

	def test_correct_tuple(self):
		"""
		The final tuple includes the correct keys.
		"""

	# exceptions

	def test_point_outside_city(self):
		"""
		Exception for when the given (lat, lon) is outside the geographical bounds
		of the city
		"""

	def test_invalid_point(self):
		"""
		Exception for when lat or long values given are invalid.
		"""
	def test_boundary_point(self):
		"""
		Given criteria for boundary point classification (on polygon), the geocoder correctly 
		classifies the point.
		"""

	def test_overflow_error(self):
		"""
		foo
		"""

suite = unittest.TestLoader().loadTestsFromTestCase(UniGeoTest)
_ = unittest.TextTestRunner().run(suite)