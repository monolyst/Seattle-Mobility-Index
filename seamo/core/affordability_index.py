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

    def __init__(self, viable_modes):
        # super().__init__(self, time_of_day, type_of_day, travel_mode,
        #     db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR)
        self.viable_modes = viable_modes
        self.affordability_scores = None

    # def _get_viable_modes(self):
    #     mc = ModeChoiceCalculator()
    #     return mc.create_blockgroup_dict(pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP))


    def create_avg_blockgroup_cost_df(self):
        """
        This method calculates all of the average cost for all trips in a blockgroup.
        Inputs: None
        Outputs: Dataframe, columns: key, cost
        """
        result_data = []#pd.DataFrame({cn.KEY: [], cn.COST: []})
        for key, values in self.viable_modes.items():
            blkgrp = str(key)
            num_trips = len(values)
            # print(num_trips)
            cost = 0
            for trip in values:
                trip.set_cost()
                cost += trip.cost
                # cost += 2
            cost /= num_trips
            # print(pd.DataFrame({cn.BLOCK_GROUP: [key], cn.COST: [cost]}))
            result_data.append({cn.KEY: [key], cn.COST: [cost]})
            # result_df = result_df.append(pd.DataFrame({cn.KEY: [key], cn.COST: [cost]}))
        return pd.DataFrame(result_data)



    def calculate_score(self):
        income = pd.read_excel(cn.BLOCK_GROUP_DEMOGRAPHICS_FP).loc[:, (cn.INCOME_BLOCKGROUP, cn.MEDIAN_HOUSEHOLD_INCOME)]
        blkgrp_mode_cost_df = self.create_avg_blockgroup_cost_df()
        blkgrp_mode_cost_df[cn.ADJUSTED_FOR_INCOME] = blkgrp_mode_cost_df.apply(lambda x: x[cn.COST] /
            income.loc(x[cn.KEY], cn.MEDIAN_HOUSEHOLD_INCOME))
        # normalization
        blkgrp_mode_cost_df[cn.NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: normalize(x[cn.COST]))
        blkgrp_mode_cost_df[cn.INCOME_NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: normalize(x[cn.ADJUSTED_FOR_INCOME]))
        self.affordability_scores = blkgrp_mode_cost_df
        return self.blkgrp_mode_cost_df
