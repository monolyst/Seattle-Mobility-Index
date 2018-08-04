import init
import cProfile
import os
import sys
import pstats
import geocoder
# import geocoder_input as gi

# DATADIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/shapefiles/')
# PROCESSED_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/')
# pickle_name = "reference.pickle"
# REFERENCE = gi.get_reference(DATADIR, PROCESSED_DIR, pickle_name)
# INFILE = str(sys.argv[1]) + ".csv"
# OUTFILE = str(sys.argv[2])

def test_geocode():
    geo = geocoder.Geocoder()
    decoded = geo.get_blockgroup((47.6145, -122.3210)).item()

cProfile.run('test_geocode()', 'OUTFILE')
p = pstats.Stats('OUTFILE')
p.sort_stats('cumtime')
p.print_stats()