"""
To call function:
$ python lat_lon_generator.py BOUNDARY_CHOICE PAIR_SIZE FILENAME
"""

import numpy as np
import random
import pandas as pd
import os
import sys
from shapely.geometry import Polygon

"""
0 - Seattle
1 - Broader King County
2 - King County and outside
"""

def define_boundary(choice):
    choice = int(choice)
    lat = 47.6149
    lon = 122.341
    LAT_BOUNDARY = 0
    LON_BOUNDARY = 0

    if choice == 0:
        LAT_BOUNDARY = 0.23814
        LON_BOUNDARY = 0.189269

    elif choice == 1:
        LAT_BOUNDARY = 0.353731
        LON_BOUNDARY = 0.236908

    elif choice == 2:
        LAT_BOUNDARY = 2.35373
        LON_BOUNDARY = 1.76309

    lat_min = lat + LAT_BOUNDARY
    lat_max = lat - LAT_BOUNDARY
    lon_min = lon + LON_BOUNDARY
    lon_max = lon - LON_BOUNDARY
    return lat_min, lat_max, lon_min, lon_max

def make_dataframe(choice, size):
    lat_min, lat_max, lon_min, lon_max = define_boundary(choice)
    lat = []
    lon = []
    for rows in range(int(size)):
        lat.append(random.uniform(lat_min, lat_max))
        lon.append(random.uniform(lon_min, lon_max))
    lat = pd.DataFrame(lat)
    lon = pd.DataFrame(lon)
    df = pd.concat([lat, lon], axis=1)
    df.columns = ['lat', 'lon']
    return df

def main(argv):
    FILENAME = str(sys.argv[3]) + '.csv'
    df = make_dataframe(sys.argv[1], sys.argv[2])
    df.to_csv(os.path.join(os.pardir, os.pardir,
        'seamo/data/test/', FILENAME), index=False)

if __name__ == "__main__":
    main(sys.argv[1:])