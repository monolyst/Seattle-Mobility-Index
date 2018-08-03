import init
import data_accessor as daq
import constants as cn
import generate_parking_data as gen_park
import time

start = time.time()
parking = gen_park.GenerateParkingData()
parking.write_to_csv(parking.blkgrp_parking_df, cn.BLOCK_GROUP_PARKING_RATES + '.csv')
print(parking.blkgrp_parking_df.head())
end = time.time()
print(end-start, 'seconds')