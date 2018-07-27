"""
TODO: pass buffer size into parking_cost and parking_cost_input, to redraw new polygons
"""

import init
import pandas as pd
import parking_cost
import data_accessor as daq
import constants as cn
import seamo_exceptions as se
from collections import defaultdict
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
        blkgrp_parking_price_dict = defaultdict(list)
        for _, row in self.blkgrp_df.iterrows():
            price = 0
            blkgrp = row[cn.KEY]
            for rate_column in [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE,
                                cn.WEEKDAY_EVENING_RATE, cn.WEEKEND_MORNING_RATE,
                                cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]:
                price += self._get_price(row[cn.LAT], row[cn.LON], rate_column)
            price /= 6
            blkgrp_parking_price_dict[blkgrp].append(price)
        return pd.DataFrame(blkgrp_parking_price_dict)



    def _load_blkgrp_data(self):
        """
        TODO: can read from csv, or directly call geography processor.
        """
        return pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP)


    def _get_price(self, blkgrp_lat, blkgrp_lon, rate_column):
        pc = parking_cost.ParkingCost()
        try:
            pc.geocode_point((float(blkgrp_lat), float(blkgrp_lon)))
        except se.NoParkingAvailableError as e:
            return 0
        else:
            df = pc.geocode_point((float(blkgrp_lat), float(blkgrp_lon)))
            return min(df.loc[:, rate_column])


    def write_to_csv(self, df, output_file, processed_dir=cn.CSV_DIR):
        """
        Call data accessor module to write dataframe to csv.
        """
        daq.write_to_csv(df, output_file, processed_dir)
