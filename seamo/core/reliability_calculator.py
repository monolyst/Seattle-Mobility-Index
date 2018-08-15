import init
import pandas as pd
import constants as cn
import data_accessor as daq
from index_base_class import IndexBase
from math import sqrt

class ReliabilityIndex(IndexBase):

    def __init__(self, db_filepath, db_name):
        self.db_filepath = db_filepath
        self.db_name = db_name
        self.reliability_scores = self.get_score()


    def _calculate_thresholds(self, df):
        df[cn.STANDARD_DEVIATION] = df.apply(lambda x: sqrt(x[cn.VARIANCE]), axis=1)
        df[cn.THRESHOLD] = df.apply(lambda x: 1.04 * x[cn.STANDARD_DEVIATION]
            + x[cn.MEAN], axis=1)
        daq.df_to_sql(df, cn.OD_HR_THRESHOLDS, self.db_name, dtype=cn.THRESHOLD_SCHEMA,
            processed_dir=self.db_filepath)


    def _calculate_reliability_score(self):

        # create sql tables for total number of trips per blockgroup and mean, variance
        # over origin, destintion, hour groups
        queries = [daq.drop_table_if_exists(cn.RELIABILITY_TOTAL),
                   cn.CREATE_TABLE_TOTAL_COUNTS,
                   daq.drop_table_if_exists(cn.OD_HR_STATS),
                   cn.CREATE_TABLE_OD_HR_STATS]
        daq.execute_query(queries, db_name=self.db_name, processed_dir=self.db_filepath)
        # select mean, variance table and bring it to pandas to calculate thresholds
        df = daq.sql_to_df(daq.select_all_from(cn.OD_HR_STATS),
            db_name=self.db_name, processed_dir=self.db_filepath)
        daq.execute_query(daq.drop_table_if_exists(cn.OD_HR_THRESHOLDS),
            db_name=self.db_name, processed_dir=self.db_filepath)
        self._calculate_thresholds(df)
        # create sql tables for number of trips that fall under reliability threshold,
        # and the ratio of these counts to the total number of trips
        queries = [daq.drop_table_if_exists(cn.RELIABILITY_THRESHOLD_COUNTS),
                   cn.CREATE_TABLE_THRESHOLD_COUNTS,
                   daq.drop_table_if_exists(cn.RELIABILITY_SCORES),
                   cn.CREATE_TABLE_RELIABILITY_SCORES]
        daq.execute_query(queries, db_name=self.db_name, processed_dir=self.db_filepath)
        # select reliability scores (ratios)
        df = daq.sql_to_df(daq.select_all_from(cn.RELIABILITY_SCORES),
            db_name=self.db_name, processed_dir=self.db_filepath)
        df = self._scale_reliability_score(df)
        return df


    def _scale_reliability_score(self, df):
        df[cn.SCALED] = df.apply(lambda x: (x[cn.RATIO] - df[cn.RATIO].min()) /
                (df[cn.RATIO].max() - df[cn.RATIO].min()), axis=1)
        df.columns = [cn.KEY, cn.RATIO, cn.SCALED]
        return df


    def get_score(self):
        try:
            daq.sql_to_df(daq.select_all_from(cn.RELIABILITY_SCORES),
                db_name=self.db_name, processed_dir=self.db_filepath)
        except:
            return self._calculate_reliability_score()
        else:
            return daq.sql_to_df(daq.select_all_from(cn.RELIABILITY_SCORES),
                db_name=self.db_name, processed_dir=self.db_filepath)

