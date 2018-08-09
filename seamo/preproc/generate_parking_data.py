"""
TODO: pass buffer size into parking_cost and parking_cost_input, to redraw new polygons
"""

import init
import pandas as pd
import numpy as np
import parking_cost
import data_accessor as daq
import constants as cn
import seamo_exceptions as se
from parse_datetime import ParseDatetime

class GenerateParkingData(object):
    def __init__(self, buffer_size=cn.BUFFER_SIZE):
        self.buffer_size = buffer_size
        self.blkgrp_df = self._load_blkgrp_data()
        self.blkgrp_parking_df = self._get_blkgrp_avg_price()


    def _get_blkgrp_avg_price(self):
        """
        This will query prices for all 6 day/time combinations and
        return an average price value.
        """
        result_df = self.blkgrp_df
        result_df[cn.RATE] = result_df.apply(lambda x: self._calculate_avg_rate(x.lat, x.lon), axis=1)
        result_df.key.astype(str)
        return result_df


    def _calculate_avg_rate(self, lat, lon):
        rates = [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE,
                cn.WEEKEND_MORNING_RATE, cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]
        rates_list = [self._get_price(lat, lon, rate) for rate in rates] 
        return np.mean(rates_list)


        # blkgrp_parking_price_df = pd.DataFrame({cn.KEY: [], cn.RATE: []})
        # for _, row in self.blkgrp_df.iterrows():
        #     price = 0
        #     blkgrp = row[cn.KEY]
        #     for rate_column in [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE,
        #                         cn.WEEKDAY_EVENING_RATE, cn.WEEKEND_MORNING_RATE,
        #                         cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]:
        #         price += self._get_price(row[cn.LAT], row[cn.LON], rate_column)
        #     price /= 6
        #     blkgrp_parking_price_df = blkgrp_parking_price_df.append(pd.DataFrame({cn.KEY: [blkgrp], cn.RATE: [price]}))
        # blkgrp_parking_df = blkgrp_parking_df.fillna(0)
        # blkgrp_parking_df.key.astype(str)
        # return blkgrp_parking_price_df



    def _load_blkgrp_data(self):
        """
        TODO: can read from csv, or directly call geography processor.
        """
        return pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP).loc[:, (cn.KEY, cn.LAT, cn.LON)]


    def _get_price(self, blkgrp_lat, blkgrp_lon, rate):
        pc = parking_cost.ParkingCost()
        try:
            pc.geocode_point((float(blkgrp_lat), float(blkgrp_lon)))
        except: #se.NoParkingAvailableError as e:
            return 0
        else:
            df = pc.geocode_point((float(blkgrp_lat), float(blkgrp_lon)))
            return min(df.loc[:, rate_column])


    def write_to_csv(self, df, output_file, processed_dir=cn.CSV_DIR):
        """
        Call data accessor module to write dataframe to csv.
        """
        daq.write_to_csv(df, output_file, processed_dir)
