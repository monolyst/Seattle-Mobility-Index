import init
import pandas as pd
import constants as cn
from index_base_class import IndexBase
import numpy as np
from collections import defaultdict

class AffordabilityIndex(IndexBase):
    """
    The affordability index calculates the relative cost of all trips from an
    origin block group.
    This index currently outputs two affordability scores:
        1) relative cost based off direct and indirect costs scaled from 0-100
        2) relative cost based off the average cheapest and fastest trips,
           scaled from 0-100
    """
    def __init__(self, viable_modes):
        """
        Constructor for instatiating the affordability index. Scores are set as
        instance variable when calculated.
        Input: viable_modes (dictionary data type), which is the output from
                the mode choice calculator. Key is origin block group, value is
                list of viable trips.
        """
        self.viable_modes = dict(viable_modes)
        self.affordability_scores = None


    def create_avg_blockgroup_cost_df(self):
        """
        This method calculates all of the average cost for all trips in a blockgroup.
        It also populates the dataframe with the average cheapest and average fastest
        trips per desination category.
        All columns are populated using vectorized operations.
        Outputs: Dataframe, columns: key, cost, direct cost, average duration,
                 average cheapest trip, and average fastest trip
        """
        result_df = pd.DataFrame({cn.KEY: list(self.viable_modes.keys())})
        result_df['temp_cost'] = result_df.applymap(lambda x: self._calculate_avg_cost(x))
        result_df[cn.COST] = result_df.apply(lambda x: x['temp_cost'][0], axis=1)
        result_df[cn.DIRECT_COST] = result_df.apply(lambda x: x['temp_cost'][1], axis=1)
        result_df[cn.AVG_DURATION] = result_df.apply(lambda x: x['temp_cost'][2], axis=1)
        result_df[cn.CHEAPEST] = result_df.apply(lambda x: x['temp_cost'][3], axis=1)
        result_df[cn.FASTEST] = result_df.apply(lambda x: x['temp_cost'][4], axis=1)
        result_df.drop(columns = ['temp_cost'], inplace=True)
        return result_df


    def _calculate_avg_cost(self, origin_blockgroup):
        """
        For a specific attribute, this method creates a list containing values
        for all trips associated with a block group.
        Inputs: origin_blockgroup
        Outputs: mean values for cost, direct cost, duration, average cheapest
                 trip, and average fastest trip
        """
        # collect all trips associated with the origin block group
        trips = self.viable_modes[origin_blockgroup]
        # run set_cost method from trip class for each trip. This populates the
        # trip object with cost attributes
        costs = [trip.set_cost().cost for trip in trips]
        direct_costs = [trip.direct_cost for trip in trips]
        time = [trip.duration for trip in trips]
        
        # define default dictionary
        groups = defaultdict(list)
        # keys are destination lat, grouping trips by their destination
        [groups[trip.destination.lat].append(trip) for trip in trips]
        # for the trips in each destination group, find the minimum value
        cheapest = {k: min([trip.direct_cost for trip in v]) for k, v in groups.items()}
        fastest = {k: min([trip.duration for trip in v]) for k, v in groups.items()}
        # the mean values of all of the lists created are returned to the dataframe
        return [np.mean(costs), np.mean(direct_costs),
            np.mean(time), np.mean(list(cheapest.values())), np.mean(list(fastest.values()))]


    def calculate_score(self, df=None):
        """
        This method calculates the affordability score. 
        Input: dataframe (optional), containing appropriate values
        Output: dataframe with each block group assigned affordability score
        """
        # check if dataframe was passed to method, if not then generate it
        if df is None:
            blkgrp_mode_cost_df = self.create_avg_blockgroup_cost_df()
        else:
            blkgrp_mode_cost_df = df
        # score 1, relative cost from direct and indirect costs:
        blkgrp_mode_cost_df = self._scale_score(blkgrp_mode_cost_df, cn.COST, cn.SCALED)
        # score 2, relative cost based off the average cheapest and fastest trips
        # compute additional time beyond average fastest trip, max is taken to
        # ensure value is positive
        blkgrp_mode_cost_df[cn.ADDITIONAL_TIME_COST] = blkgrp_mode_cost_df.apply(lambda x:
            max((x[cn.AVG_DURATION] - x[cn.FASTEST]), 0) / cn.MIN_TO_HR * cn.VOT_RATE, axis=1)
        # calculate relative cost 
        blkgrp_mode_cost_df[cn.RELATIVE_COST] = blkgrp_mode_cost_df.apply(lambda x:
            x[cn.DIRECT_COST] - x[cn.CHEAPEST] + x[cn.ADDITIONAL_TIME_COST], axis=1)
        # scaled score
        blkgrp_mode_cost_df = self._scale_score(blkgrp_mode_cost_df,
            cn.RELATIVE_COST, cn.RELATIVE_SCALED)
        # set dataframe to instance variable
        self.affordability_scores = blkgrp_mode_cost_df
        return self.affordability_scores


    def _scale_score(self, df, column, scaled_name):
        """
        Method for scaling score from 0-100
        Inputs: dataframe, column to scale, scaled column name
        Outputs: dataframe with new scaled value
        """
        df[scaled_name] = df.apply(lambda x: (x[column] - df[column].min()) /
                (df[column].max() - df[column].min()), axis=1)
        return df