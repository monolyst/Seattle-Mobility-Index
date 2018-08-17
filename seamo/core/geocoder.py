import init
import pandas as pd
from geocoder_input import GeocoderInput, GeocoderBlockgroupInput
import constants as cn
from geocode_base_class import GeocodeBase
import seamo_exceptions as se

class Geocoder(GeocodeBase):
    """
    Python module for the universal geocoder. Given a lat, lon point, the
    geocoder will return geographical attributes about where that point lies,
    including Census block group, long neighborhood name, short neighborhood
    name, urban village, council district, and zipcode. More attributes can
    easily be added by adding the appropriate shapefiles, and including these
    new attributes in the reference dataframe generated in the geocoder_input
    module.

    Methods can be called from other python modules based on file format passed.
    To get all geocoded attributes call:
    - geocode_df(gdf, pickle_name) if passing geodataframe, pickle_name parameter
      is optional, and default value if nothing is passed is reference.pickle
    - geocode_point(coord, pickle_name) if passing lat/lon pair in format (LAT, LON),
      pickle_name parameter is optional, default will be used otherwise
    - geocode_csv(input_file, pickle_name) if csv passed with lat, lon header,
      pickle_name parameter is optional, and default value if nothing is passed is 
      reference.pickle

    To get only block group call:
    - get_blockgroup_from_df(gdf, pickle_name) if passing geodataframe, pickle_name 
      parameter is optional, default will be used otherwise
    - get_blockgroup_from_point(coord, pickle_name) if passing lat/lon pair in 
      format (LAT, LON), pickle_name parameter is optional, default will be used
      otherwise
    """ 
    def __init__(self, crs=cn.CRS_EPSG):
        super().__init__(crs)


    # Geocoder function
    def geocode(self, gdf, pickle_name=cn.REFERENCE_PICKLE):
        """ 
        This is the main geocoding method. It assumes that lat, lon pairs are
        ordered lon, lat.
        Inputs: geodataframe containing lat/lon points
        Outputs: dataframe containing geocoded information
        """
        reference_gdf = self._get_geocode_reference(0, pickle_name)
        try:
            self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        except se.NoOverlapSpatialJoinError:
            df = pd.DataFrame(cn.GEOCODE_NAN_DF)
        else:
            df = self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
            df = df.sort_values(by=cn.GEOGRAPHY)
            df = df.set_index([cn.LAT, cn.LON, cn.GEOGRAPHY], append=cn.KEY).unstack()
            df.columns = df.columns.droplevel()
            df = self._format_output(df)
        self.dataframe = df
        return df


    def geocode_blockgroup(self, gdf, pickle_name=cn.BLOCKGROUP_PICKLE):
        """
        This is the geocoding method that only returns block group. Use if
        performance is a constraint, because the sjoining takes less time.
        Inputs: geodataframe containing lat/lon points
        Outputs: dataframe containing block groups
        """
        reference_gdf = self._get_geocode_reference(1, pickle_name)
        try:
            self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
        except se.NoOverlapSpatialJoinError:
            print('No overlap found')
            df = pd.DataFrame({cn.KEY: [None]})
        else:
            df = self._find_overlap_in_reference(gdf, pickle_name, reference_gdf)
            df[cn.KEY] = df[cn.KEY].astype(str)
        return df


    def _format_output(self, df):
        """
        This method formats the geocoded attributes as strings so they have the
        right types in sql, and also fills in missing values with None
        Inputs: dataframe of geocoded attributes
        Outputs: formatted dataframe of geocoded attributes
        """
        df = df.reset_index().drop(['level_0'], axis=1)
        df[cn.LAT] = df[cn.LAT].astype(float)
        df[cn.LON] = df[cn.LON].astype(float)
        for col in [cn.BLOCK_GROUP, cn.NBHD_LONG, cn.NBHD_SHORT, cn.COUNCIL_DISTRICT,
                    cn.URBAN_VILLAGE, cn.ZIPCODE]:
            try:
                df[col].astype(str)
            except KeyError:
                df[col] = None
            else:
                df[col] = df[col].astype(str)
        df = df[[cn.LAT, cn.LON, cn.BLOCK_GROUP, cn.NBHD_LONG, cn.NBHD_SHORT,cn.COUNCIL_DISTRICT,
                cn.URBAN_VILLAGE, cn.ZIPCODE]]
        return df


    def _get_geocode_reference(self, ref_type, pickle_name):
        """
        This method gets the appropriate reference dataframe to be used in the
        spatial joining.
        Inputs: geocode method using, pickle name
        Outputs: reference dataframe
        """
        if ref_type == 0:
            gi = GeocoderInput()
            return self._get_reference(pickle_name, gi)
        elif ref_type == 1:
            gi = GeocoderBlockgroupInput()
            return self._get_reference(pickle_name, gi)


    def geocode_csv(self, input_file, pickle_name=cn.REFERENCE_PICKLE):
        """
        This method converts a csv file to a geodataframe and then calls the
        geocoding method.
        Inputs: input csv file, pickle name (optional)
        Outputs: dataframe of geocoded information
        """
        return super().geocode_csv(input_file, pickle_name)


    def geocode_point(self, coord, pickle_name=cn.REFERENCE_PICKLE):
        """
        This method converts a lat/lon point to a geodataframe and then calls the
        geocoding method.
        Inputs: lat/lon point in string/tuple format, pickle name (optional)
        Outputs: dataframe of geocoded information
        """
        df = super().geocode_point(coord) 
        return self.geocode(df, str(pickle_name))

    def geocode_df(self, df, pickle_name=cn.REFERENCE_PICKLE):
        """
        This method converts a dataframe to a geodataframe and then calls the
        geocoding method.
        Inputs: dataframe, pickle name (optional)
        Outputs: dataframe of geocoded information
        """
        df = super().geocode_df(df)
        return self.geocode(df, str(pickle_name))

    def get_blockgroup_from_point(self, coord, pickle_name=cn.BLOCKGROUP_PICKLE):
        """
        This method converts a lat/lon point to a geodataframe and then calls the
        blockgroup geocoding method.
        Inputs: lat/lon point in string/tuple format, pickle name (optional)
        Outputs: dataframe with block groups
        """
        df = super().geocode_point(coord) 
        return self.geocode_blockgroup(df, str(pickle_name))

    def get_blockgroup_from_df(self, df, pickle_name=cn.BLOCKGROUP_PICKLE):
        """
        This method converts a dataframe to a geodataframe and then calls the
        blockgroup geocoding method.
        Inputs: dataframe, pickle name (optional)
        Outputs: dataframe with block groups
        """
        df = super().geocode_df(df)
        return self.geocode_blockgroup(df, str(pickle_name))
