import cProfile
import os
import sys
import pstats
import geocoder as gg
import geocoder_input as gi

DATADIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/shapefiles/')
PROCESSED_DIR = os.path.join(os.pardir, os.pardir, 'seamo/data/processed/')
pickle_name = "reference.pickle"
REFERENCE = gi.get_reference(DATADIR, PROCESSED_DIR, pickle_name)
INFILE = str(sys.argv[1]) + ".csv"
OUTFILE = str(sys.argv[2])

cProfile.run('gg.geocode(os.path.join(os.pardir, os.pardir, "seamo/data/test/", INFILE), REFERENCE)', OUTFILE)
p = pstats.Stats(OUTFILE)
p.sort_stats('tottime')
p.print_stats()