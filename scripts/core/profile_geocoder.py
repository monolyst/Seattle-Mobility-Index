import cProfile
import os
import sys
import pstats
import geopandas_geocoder as gg
import geocoder_input as gi

DATADIR = os.path.join(os.pardir, os.pardir, 'seamo/data/raw/shapefiles/')
REFERENCE = gi.make_reference(DATADIR)
INFILE = str(sys.argv[1]) + ".csv"
OUTFILE = str(sys.argv[2])

cProfile.run('gg.geocode(os.path.join(os.pardir, os.pardir, "seamo/data/test/", INFILE), REFERENCE)', OUTFILE)
p = pstats.Stats(OUTFILE)
p.sort_stats('cumtime')
p.print_stats()