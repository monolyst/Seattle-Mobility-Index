"""
This is a test file for universal_geocoder.py
"""

import unittest

class UniGeoTest(unittest.TestCase):

	def test_maxsize(self):

	def test_read_nshort(self):
		"""
		The purpose of this test is to ensure correct
		loading of the data from Neihborhoods-Short.csv
		"""
		
		
		#data type
		#dataframe dimensions

	def test_read_nlong(self):

	def test_read_sccdst(self):

	def test_read_zipcode(self):

	def test_read_urbvil(self):

	def test_read_blkgrp(self):
		

	def test_path_nshort(self):
		"""
		Ensure a path object was created for the Neighborhood-Short 
		geography.

		"""




suite = unittest.TestLoader().loadTestsFromTestCase(UniGeoTest)
_ = unittest.TextTestRunner().run(suite)