import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle
import constants as cn
import geocode_input_base_class as gib

#Read in shapes files for block group, neighborhoods, zipcode, council district and urban villages
# DATADIR = os.path.join(os.getcwd(), '../../seamo/data/raw/shapefiles/')

class GeocoderInput(gib.GeocodeInputBase):
    def __init__(self):
        # import pdb; pdb.set_trace()
        super().__init__()

    def read_shapefile(self, raw_dir, shapefile, column_name, name):
        gdf = super().read_shapefile(raw_dir, shapefile)
        gdf = gdf.loc[:, (column_name, cn.GEOMETRY)]
        gdf = gdf.to_crs(cn.CRS_EPSG)
        gdf.columns = [cn.KEY, cn.GEOMETRY]
        gdf[cn.GEOGRAPHY] = str(name)
        return gdf

    def make_reference(self, raw_dir, processed_dir, pickle_name):
        blkgrp = self.read_shapefile(raw_dir, cn.BLKGRP_FNAME, cn.BLKGRP_KEY, cn.BLOCK_GROUP)
        nbhd_short = self.read_shapefile(raw_dir, cn.NBHD_FNAME, cn.NBHD_SHORT_KEY, cn.NBHD_SHORT)
        nbhd_long = self.read_shapefile(raw_dir, cn.NBHD_FNAME, cn.NBHD_LONG_KEY, cn.NBHD_LONG)
        zipcode = self.read_shapefile(raw_dir, cn.ZIPCODE_FNAME, cn.ZIPCODE_KEY, cn.ZIPCODE)
        council_district = self.read_shapefile(raw_dir, cn.COUNCIL_DISTRICT_FNAME, cn.COUNCIL_DISTRICT_KEY, cn.COUNCIL_DISTRICT)
        urban_village = self.read_shapefile(raw_dir, cn.URBAN_VILLAGE_FNAME, cn.URBAN_VILLAGE_KEY, cn.URBAN_VILLAGE)
        reference = pd.concat([blkgrp, nbhd_short, nbhd_long, zipcode, council_district, urban_village])
        self.make_pickle(processed_dir, reference, pickle_name)
        return reference