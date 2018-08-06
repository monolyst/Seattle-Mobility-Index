"""
Personas class:
This class loads clustered .csv file
and returns weights, thresholds, median income, and mean number of children
"""

import os
import pandas as pd

import init
import constants as cn

personas_df = pd.read_csv(cn.PERSONAS_CLUSTER_FP, index_col = 0)

class Persona:
    
    def __init__(self, person_type):
        
        """
        This function initializes the Personas class
        input: person_type (string that matches a row)
        output: an entire row with information (Pandas Series)
        """

        self.data = personas_df.loc[person_type,:]

    def get_weights(self):

        """
        This function returns weights of the selected type
        input: N/A
        output: a Pandas Series with weights of four modes
        """
        
        return(self.data.filter(regex='_weight$'))

    def get_thresholds(self):

        """
        This function returns weights of the selected type
        input: N/A
        output: a Pandas Series with thresholds of four modes
        """

        return(self.data.filter(regex='_threshold$'))

    def get_income(self):

        """
        This function returns weights of the selected type
        input: N/A
        output: a Pandas Series with median income
        """

        return(self.data.filter(regex='_income$'))
 
    def get_numchildren(self):

        """
        This function returns weights of the selected type
        input: N/A
        output: a Pandas Series with mean number of children
        """

        return(self.data.filter(regex='_children$'))

