"""
TODO: pass buffer size into parking_cost and parking_cost_input, to redraw new polygons
"""

import init
import pandas as pd
import parking_cost as pc
import constants as cn

class GenerateParkingData(object):
    def __init__(self, buffer_size=cn.BUFFER_SIZE):
        self.buffer_size = buffer_size


    def _get_blkgrp_avg_price(self):
