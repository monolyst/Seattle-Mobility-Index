"""
This is a test file for universal_geocoder.py
"""

import unittest

class UniGeoTest(unittest.TestCase):



suite = unittest.TestLoader().loadTestsFromTestCase(UniGeoTest)
_ = unittest.TextTestRunner().run(suite)