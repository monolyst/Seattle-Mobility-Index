import __init__
import constants as cn
from basket_destination_calculator import BasketCalculator

"""
Calculate distances using haversine formula. 
Filter combinations using a threshold.
"""
# Instantiate a basket calculator without an API key.
bc = BasketCalculator('null')
origin_df = BasketCalculator.origin_df
dest_df = BasketCalculator.dest_df
dist_fp = cn.HAVERSINE_DIST_FP
# bc.origins_to_destinations(dist_fp, origin_df, dest_df, 'haversine', True)
