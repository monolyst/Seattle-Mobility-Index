import init
import os
import constants as cn
import pandas as pd
import data_accessor as daq
from geocoder import Geocoder

class ConvertDynamodb(object):
    def __init__(self):
        pass


    def _read_dynamodb_outfile(self, dynamodb_csv, dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = pd.read_csv(os.path.join(dynamodb_dir, dynamodb_csv))
        df.drop(columns = ['status'], inplace=True)
        df[cn.BLOCK_GROUP] = df.apply(lambda x: x['tripID'].split('++')[0], axis=1)
        df[cn.DESTINATION] = df.apply(lambda x: x['tripID'].split('++')[1], axis=1)
        return df


    def _merge_place_data(self, df, filepath=cn.DEST_FP):
        places = pd.read_csv(filepath)
        df = df.merge(places, left_on=cn.DESTINATION, right_on=cn.PLACE_ID, how='left')
        df.drop(columns = ['tripID', cn.DESTINATION, cn.PLACE_ID], inplace=True)
        df.rename(columns={'name': cn.DESTINATION, 'lng': cn.LON}, inplace=True)
        return df

    def _chunker(self, df, chunks):
        size = len(df) // chunks
        return (df[pos:pos + size] for pos in range(0, len(df), size))

    def _get_blockgroup(self, df):
        geo = Geocoder()
        temp = []
        for chunk in self._chunker(df, 100):
            coords = chunk.loc[:, (cn.LAT, cn.LON)]
            blkgrps = geo.get_blockgroup_from_df(coords)
            blkgrps.columns = [cn.LAT, cn.LON, cn.DEST_BLOCK_GROUP]
            temp.append(pd.merge(chunk, blkgrps, left_on=[cn.LAT, cn.LON], right_on=[cn.LAT, cn.LON], how='left').drop_duplicates())
        df = pd.concat(temp, sort=False).reset_index()
        return df

    def _process_dynamodb(self, dynamodb_csv, dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = self._read_dynamodb_outfile(dynamodb_csv, dynamodb_dir)
        df = self._merge_place_data(df)
        df = self._get_blockgroup(chunked_df)
        return df


    def write_to_csv(self, df, output_file, processed_dir=cn.CSV_DIR):
        daq.write_to_csv(df, output_file + '.csv', processed_dir)


    def write_to_sql(self, df, table_name):
        daq.df_to_sql(df, table_name)


class ConvertDynamodbDriving(ConvertDynamodb):
    def __init__(self):
        self.dataframe = self._process_dynamodb_driving()
    

    def _process_dynamodb_driving(self, dynamodb_csv='dynamo_out_driving.csv', dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = self._process_dynamodb(dynamodb_csv, dynamodb_dir)
        df = df[[cn.BLOCK_GROUP, cn.MODE, cn.DEPARTURE_TIME, cn.DISTANCE, cn.DURATION,
                cn.DURATION_IN_TRAFFIC, cn.DEST_BLOCK_GROUP, cn.DESTINATION, cn.LAT, cn.LON,
                cn.ADDRESS, cn.CLASS, cn.TYPE, cn.CITY, cn.RATING]]
        return df


class ConvertDynamodbTransit(ConvertDynamodb):
    def __init__(self):
        self.dataframe = self._process_dynamodb_transit()


    def _process_dynamodb_transit(self, dynamodb_csv='dynamo_out_transit.csv', dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = self._process_dynamodb(dynamodb_csv, dynamodb_dir)
        df = df[[cn.BLOCK_GROUP, cn.MODE, cn.FARE, cn.DEPARTURE_TIME, cn.DISTANCE, 
                cn.DURATION, cn.DEST_BLOCK_GROUP, cn.DESTINATION, cn.LAT, cn.LON, cn.ADDRESS,
                cn.CLASS, cn.TYPE, cn.CITY, cn.RATING]]
        return df


class ConvertDynamodbBiking(ConvertDynamodb):
    def __init__(self):
        self.dataframe = self._process_dynamodb_biking()


    def _process_dynamodb_biking(self, dynamodb_csv='dynamo_out_bicycling.csv', dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = self._process_dynamodb(dynamodb_csv, dynamodb_dir)
        df = df[[cn.BLOCK_GROUP, cn.MODE, cn.DEPARTURE_TIME, cn.DISTANCE, 
                cn.DURATION, cn.DEST_BLOCK_GROUP, cn.DESTINATION, cn.LAT, cn.LON, cn.ADDRESS,
                cn.CLASS, cn.TYPE, cn.CITY, cn.RATING]]
        return df


class ConvertDynamodbWalking(ConvertDynamodb):
    def __init__(self):
        self.dataframe = self._process_dynamodb_walking()


    def _process_dynamodb_walking(self, dynamodb_csv='dynamo_out_walking.csv', dynamodb_dir=cn.DYNAMODB_OUT_DIR):
        df = self._process_dynamodb(dynamodb_csv, dynamodb_dir)
        df = df[[cn.BLOCK_GROUP, cn.MODE, cn.DEPARTURE_TIME, cn.DISTANCE, 
                cn.DURATION, cn.DEST_BLOCK_GROUP, cn.DESTINATION, cn.LAT, cn.LON, cn.ADDRESS,
                cn.CLASS, cn.TYPE, cn.CITY, cn.RATING]]
        return df