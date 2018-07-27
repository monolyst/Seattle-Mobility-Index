import init
import index_base_class
import pandas as pd
import constants as cn
import trip as tp
import data_accessor as daq
from mode_choice_calculator import ModeChoiceCalculator
from index_base_class import IndexBase

class AffordabilityIndex(IndexBase):
    DATADIR = cn.CSV_DIR #db dir?

    def __init__(self):
        # super().__init__(self, time_of_day, type_of_day, travel_mode,
        #     db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR)
        self.affordability_scores = None

    # def _get_viable_modes(self):
    #     mc = ModeChoiceCalculator()
    #     return mc.create_blockgroup_dict(pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP))


    def create_blockgroup_cost_df(self, viable_modes):
        blkgrp_mode_cost_df = pd.DataFrame({cn.BLOCK_GROUP: [], cn.COST: []})
        for key, values in viable_modes.items():
            blkgrp = key
            num_trips = len(values)
            cost = 0
            for trip in values:
                trip.set_cost()
                cost += trip.cost
            cost /= num_trips
            # print(pd.DataFrame({cn.BLOCK_GROUP: [key], cn.COST: [cost]}))
            blkgrp_mode_cost_df =blkgrp_mode_cost_df.append(pd.DataFrame({cn.BLOCK_GROUP: [key], cn.COST: [cost]}))
        return blkgrp_mode_cost_df



    def calculate_score(self, viable_modes):
        income = pd.read_excel(cn.BLOCK_GROUP_DEMOGRAPHICS_FP).loc[:, (cn.INCOME_BLOCKGROUP, cn.MEDIAN_HOUSEHOLD_INCOME)]
        blkgrp_mode_cost_df = self.create_blockgroup_cost_df(viable_modes)
        blkgrp_mode_cost_df[cn.ADJUSTED_FOR_INCOME] = blkgrp_mode_cost_df.apply(lambda x: x[cn.COST] /
            income.loc(x[cn.BLOCK_GROUP], cn.MEDIAN_HOUSEHOLD_INCOME))
        # normalization
        blkgrp_mode_cost_df[cn.NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: normalize(x[cn.COST]))
        blkgrp_mode_cost_df[cn.INCOME_NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: normalize(x[cn.ADJUSTED_FOR_INCOME]))
        self.affordability_scores = blkgrp_mode_cost_df
        return self.blkgrp_mode_cost_df
