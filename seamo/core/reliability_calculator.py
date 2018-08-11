import init
import index_base_class
import pandas as pd
import constants as cn
import trip as tp
import parse_datetime as pdt
import data_accessor as daq
from index_base_class import IndexBase

class ReliabilityIndex(IndexBase):

    def __init__(self):
 

    def get_blkgrp_data(self, blockgroup):
        """
        Get data fron a single blockgroup for all 14 hours for each day being measured. 
        This will query from our database of all Google Distance Out Data.
        Input: Blockgroup
        Output: Dataframe of duration_in_traffic for all 14 hours for each blockgroup
        """

        for day in days:
            return self.calc_blkgrp_variance(daq.read_sql(day, blockgroup))

        # df = pd.read_csv(cn.SIMULATED_CAR_DATA_FP)

        # for blockgroup in blockgroups:
            # return df[df.origin == blockgroup]

    def calc_blkgrp_variance(self, df):
        """
        Calculate variance across all days being measured at each hour of the day.
        Input: Dataframe of duration_in_traffic for a single blockgroup
        Output: Dataframe of variance for each hour
        """
        df_var = df.groupby(['block_group','time'])['simulated_traffic_time'].var()
        return df_var.to_frame('variance').reset_index()


    def calc_threshold(self, df):
        """
        Calculate the percentage of trips under 85th percentile for each block group.
        Input: Dataframe of duration_in_traffic for a single blockgroup
        Output: Dataframe of percentage of trips under 85th percentile for each hour for each blockgroup.
        """
        df_threshold = df.groupby(['block_group', 'time'])['simulated_traffic_time'].quantile(0.85)
        df_threshold = df_threshold.to_frame('85th').reset_index()

        df_q85th_index[df_q85th_index['simulated_traffic_time'] < df_q85th_index['85th']].groupby(['block_group', 'time'])['simulated_traffic_time'].count()




    def calc_buffer_index(self,df):
        """
        Calculate the buffer index for each block group.
        Input: Dataframe of duration_in_traffic for a single blockgroup
        Output: Dataframe of buffer index for each hour for each blockgroup.
        """

        quantile = df.groupby(['block_group', 'time'])['simulated_traffic_time'].quantile(0.95)
        df_buffer['quantile']= quantile.to_frame('quantile').reset_index()

        mean = df_buf.groupby(['block_group', 'time'])['simulated_traffic_time'].mean()
        mean_df = mean.to_frame('mean').reset_index()

        df_buf_index['index'] = df_buf_index['quantile'] - df_buf_index['mean']/ df_buf_index['mean']

        buf_index = df_buf_index.groupby(['block_group'])['index'].mean()
        buf_index = buf_index.to_frame('index').reset_index()

    def calc_blkgrp_mean(self, df):
        """
        Calculate mean for entries in dataframes.
        Input: Dataframe of a single block group
        Output: Mean for a blockgroup
        """
        return df.mean()
        


    def calc_reliability(self, blockgroup):
        df = get_blkgrp_data(blockgroup)
        df = calc_blkgrp_variance(df)
        result = calc_blkgrp_mean(df)
        return result




    def reliability_index(self):
        df = pd.DataFrame(blockgroup_keys)
        df['variance_index'] = df.apply(lambda x: calc_reliability(x))
        df['buffer_index'] = df.apply(lambda x: calc_buffer_index(x))
        df['threshold_index'] = df.apply(lambda x: calc_threshold_index(x))
        return df








