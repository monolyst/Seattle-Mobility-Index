import os

import geopandas as gpd
from matplotlib import path

DATADIR = os.path.join(os.getcwd(), '../seamo/data/raw/shapefiles/')

blkgrp = gpd.read_file(os.path.join(DATADIR, "blkgrp10_shore.shp"))
blkgrp = blkgrp.loc[:, ('GEO_ID_GRP', 'geometry')]
blkgrp = blkgrp.to_crs({'init' :'epsg:4326'})
blkgrp.columns.values[[0]] = ['key']

nbhd = gpd.read_file(os.path.join(DATADIR, "neighborhood.shp"))
nbhd = nbhd.loc[:, ('NEIGHBORHO', 'geometry')]
nbhd = nbhd.to_crs({'init' :'epsg:4326'})
nbhd.columns.values[[0]] = ['key']

zipcode = gpd.read_file(os.path.join(DATADIR, "zipcode.shp"))
zipcode = zipcode.loc[:, ('ZIPCODE', 'geometry')]
zipcode = zipcode.to_crs({'init' :'epsg:4326'})
zipcode.columns.values[[0]] = ['key']

scc = gpd.read_file(os.path.join(DATADIR, "sccdst.shp"))
scc = scc.loc[:, ('SCCDST', 'geometry')]
scc = scc.to_crs({'init' :'epsg:4326'})
scc.columns.values[[0]] = ['key']

urbanvillage = gpd.read_file(os.path.join(DATADIR, "DPD_uvmfg_polygon.shp"))
urbanvillage = urbanvillage.loc[:, ('UV_NAME', 'geometry')]
urbanvillage.columns.values[[0]] = ['key']