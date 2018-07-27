import init
import data_accessor as daq
import constants as cn
import generate_parking_data as gen_park

parking = gen_park.GenerateParkingData()
gen_park.write_to_csv(parking.blkgrp_parking_df, cn.BLOCK_GROUP_PARKING_RATES_FP)