import init
import pandas as pd
import constants as cn
import trip as tp
import data_accessor as daq
from index_base_class import IndexBase
import numpy as np
from collections import defaultdict

class AffordabilityIndex(IndexBase):
    DATADIR = cn.CSV_DIR #db dir?

    def __init__(self, viable_modes):
        # super().__init__(self, time_of_day, type_of_day, travel_mode,
        #     db_name=cn.GOOGLE_DIST_MATRIX_OUT, datadir=DATADIR)
        self.viable_modes = dict(viable_modes)
        self.affordability_scores = None


    def create_avg_blockgroup_cost_df(self):
        """
        This method calculates all of the average cost for all trips in a blockgroup.
        Inputs: None
        Outputs: Dataframe, columns: key, cost
        """
        result_df = pd.DataFrame({cn.KEY: list(self.viable_modes.keys())})
        result_df['temp_cost'] = result_df.applymap(lambda x: self._calculate_avg_cost(x))
        result_df[cn.COST] = result_df.apply(lambda x: float(x['temp_cost'].split(', ')[0]), axis=1)
        result_df[cn.DIRECT_COST] = result_df.apply(lambda x: float(x['temp_cost'].split(', ')[1]), axis=1)
        result_df[cn.AVG_DURATION] = result_df.apply(lambda x: float(x['temp_cost'].split(', ')[2]), axis=1)
        result_df[cn.CHEAPEST] = result_df.apply(lambda x: float(x['temp_cost'].split(', ')[3]), axis=1)
        result_df[cn.FASTEST] = result_df.apply(lambda x: float(x['temp_cost'].split(', ')[4]), axis=1)
        result_df.drop(columns = ['temp_cost'], inplace=True)
        return result_df


    def _calculate_avg_cost(self, origin_blockgroup):
        trips = self.viable_modes[origin_blockgroup]
        costs = [trip.set_cost().cost for trip in trips]
        direct_costs = [trip.direct_cost for trip in trips]
        time = [trip.duration for trip in trips]
        
        groups = defaultdict(list)
        [groups[trip.destination.lat].append(trip) for trip in trips]
        # import pdb; pdb.set_trace()
        cheapest = {k: min([trip.direct_cost for trip in v]) for k, v in groups.items()}
        fastest = {k: min([trip.duration for trip in v]) for k, v in groups.items()}
        return '{}, {}, {}, {}, {}'.format(np.mean(costs), np.mean(direct_costs),
            np.mean(time), np.mean(list(cheapest.values())), np.mean(list(fastest.values())))



    def calculate_score(self, df=None):
        # income = pd.read_excel(cn.BLOCK_GROUP_DEMOGRAPHICS_FP, dtype={cn.INCOME_BLOCKGROUP: str})
        # income = income[income['Year'] == 2016].loc[:, (cn.INCOME_BLOCKGROUP, cn.MEDIAN_HOUSEHOLD_INCOME)]
        # income.loc[income[cn.INCOME_BLOCKGROUP] == '530330111024', :]
        # blkgrp_mode_cost_df[cn.ADJUSTED_FOR_INCOME] = blkgrp_mode_cost_df.apply(lambda x: (x[cn.COST] /
        #     float(income.loc[income[cn.INCOME_BLOCKGROUP] == x[cn.KEY], cn.MEDIAN_HOUSEHOLD_INCOME])), axis=1)

        # import pdb; pdb.set_trace()
        if df is None:
            blkgrp_mode_cost_df = self.create_avg_blockgroup_cost_df()
        else:
            blkgrp_mode_cost_df = df   
        blkgrp_mode_cost_df[cn.ADDITIONAL_TIME_COST] = blkgrp_mode_cost_df.apply(lambda x:
            max((x[cn.AVG_DURATION] - x[cn.FASTEST]), 0) / cn.MIN_TO_HR * cn.VOT_RATE, axis=1)
        blkgrp_mode_cost_df[cn.RELATIVE_COST] = blkgrp_mode_cost_df.apply(lambda x:
            x[cn.DIRECT_COST] - x[cn.CHEAPEST] + x[cn.ADDITIONAL_TIME_COST], axis=1)


        # normalization
        mean_cost = blkgrp_mode_cost_df.cost.mean()
        std_cost = blkgrp_mode_cost_df.cost.std()
        mean_relative_cost = blkgrp_mode_cost_df.relative_cost.mean()
        std_relative_cost = blkgrp_mode_cost_df.relative_cost.std()
        # # normalization
        blkgrp_mode_cost_df[cn.NORMALIZED] = blkgrp_mode_cost_df.apply(lambda x: (x[cn.COST] -
            mean_cost) / std_cost, axis=1)
        blkgrp_mode_cost_df[cn.SCALED] = blkgrp_mode_cost_df.apply(lambda x: -1 *
            ((x[cn.COST] - blkgrp_mode_cost_df[cn.COST].min()) /
                (blkgrp_mode_cost_df[cn.COST].max() - blkgrp_mode_cost_df[cn.COST].min())) + 1, axis=1)

        blkgrp_mode_cost_df[cn.RELATIVE_SCALED] = blkgrp_mode_cost_df.apply(lambda x: 
            ((x[cn.RELATIVE_COST] - blkgrp_mode_cost_df[cn.RELATIVE_COST].min()) /
                (blkgrp_mode_cost_df[cn.RELATIVE_COST].max() -
                    blkgrp_mode_cost_df[cn.RELATIVE_COST].min())), axis=1)
        self.affordability_scores = blkgrp_mode_cost_df
        return self.affordability_scores