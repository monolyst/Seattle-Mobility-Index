import init
import index_base_class
import pandas as pd
import constants as cn
import trip as tp
import data_accessor as daq
from mode_choice_calculator import ModeChoiceCalculator
from index_base_class import IndexBase
import numpy as np

class AffordabilityIndex(IndexBase):
    DATADIR = cn.CSV_DIR #db dir?

    def __init__(self, viable_modes):
        # super().__init__(self, time_of_day, type_of_day, travel_mode,
        #     db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR)
        self.viable_modes = dict(viable_modes)
        self.affordability_scores = None
        # self.costs = None

    # def _get_viable_modes(self):
    #     mc = ModeChoiceCalculator()
    #     return mc.create_blockgroup_dict(pd.read_csv(cn.SEATTLE_BLOCK_GROUPS_FP))


    def create_avg_blockgroup_cost_df(self):
        """
        This method calculates all of the average cost for all trips in a blockgroup.
        Inputs: None
        Outputs: Dataframe, columns: key, cost
        """
        result_df = pd.DataFrame({cn.KEY: list(self.viable_modes.keys())})
        result_df[cn.COST] = result_df.applymap(lambda x: self._calculate_avg_cost(x, cn.COST))
        result_df[cn.DIRECT_COST] = result_df.applymap(lambda x: self._calculate_avg_cost(x, cn.DIRECT_COST))
        return result_df


    def _calculate_avg_cost(self, origin_blockgroup, column):
        # if self.costs is None:
        trips = self.viable_modes[origin_blockgroup]
        costs = [trip.set_cost().cost[column] for trip in trips]
        return np.mean(costs)


    def calculate_score(self, df=None):
        income = pd.read_excel(cn.BLOCK_GROUP_DEMOGRAPHICS_FP, dtype={cn.INCOME_BLOCKGROUP: str})
        income = income[income['Year'] == 2016].loc[:, (cn.INCOME_BLOCKGROUP, cn.MEDIAN_HOUSEHOLD_INCOME)]
        # income.loc[income[cn.INCOME_BLOCKGROUP] == '530330111024', :]

        # import pdb; pdb.set_trace()
        if df is None:
            blkgrp_mode_cost_df = self.create_avg_blockgroup_cost_df()
        else:
            blkgrp_mode_cost_df = df   
        blkgrp_mode_cost_df[cn.ADJUSTED_FOR_INCOME] = blkgrp_mode_cost_df.apply(lambda x: (x[cn.COST] /
            float(income.loc[income[cn.INCOME_BLOCKGROUP] == x[cn.KEY], cn.MEDIAN_HOUSEHOLD_INCOME])), axis=1)
        # normalization
        mean_cost = blkgrp_mode_cost_df.cost.mean()
        std_cost = blkgrp_mode_cost_df.cost.std()
        # # normalization
        blkgrp_mode_cost_df[cn.NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: (x[cn.COST] -
            mean_cost) / std_cost, axis=1)
        blkgrp_mode_cost_df[cn.SCALED] = blkgrp_mode_cost_df.apply(lambda x: -1 *
            ((x[cn.COST] - blkgrp_mode_cost_df[cn.COST].min()) /
                (blkgrp_mode_cost_df[cn.COST].max() - blkgrp_mode_cost_df[cn.COST].min())) + 1, axis=1)
        self.affordability_scores = blkgrp_mode_cost_df
        return self.affordability_scores