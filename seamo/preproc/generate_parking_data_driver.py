import init
import data_accessor as daq
import constants as cn
import generate_parking_data as gen_park
import time

start = time.time()
try:
    daq.open_pickle(cn.PICKLE_DIR, 'parking_rates.pickle')
except:
    parking = gen_park.GenerateParkingData()
    parking.write_to_csv(parking.blkgrp_parking_df, cn.BLOCK_GROUP_PARKING_RATES
        + '.csv')
    parking.blkgrp_parking_df = parking.blkgrp_parking_df.set_index(cn.KEY).transpose().reset_index().drop(columns = ['index'])
    parking.blkgrp_parking_df.columns.name = None
    parking_dict = parking.blkgrp_parking_df.to_dict(orient='records')
    daq.make_pickle(cn.PICKLE_DIR, parking_dict, 'parking_rates.pickle')

end = time.time()
print(end-start, 'seconds')