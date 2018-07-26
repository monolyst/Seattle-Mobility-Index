import init
import constants as cn 
from trip import Trip
from mode_choice_calculator import ModeChoiceCalculator

import pandas as pd

mc = ModeChoiceCalculator()
df = pd.read_csv(cn.DISTANCES_OUT_FP)


blockgroup_dict = mc.create_blockgroup_dict(df)

mc.create_availability_csv(blockgroup_dict)
