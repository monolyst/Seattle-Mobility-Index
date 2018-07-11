import itertools
import os

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

CLASS_LIST = ["urban village", "citywide", "destination park", "supermarket", "library",
              "hospital", "pharmacy", "post_office", "school", "cafe"]  

DATADIR = os.path.join(os.getcwd(), "../seamo/data/raw")

def distill_basket_test(testArray):
    
    """
    ## Tune and Evaluate Model ##
    We will evaluate the model by comparing the 'proximity ratio' 
    from the results with the ratio from the PSRC survey for each block group. 
    We will look at all possible parameter calculations and identify the ones with the lowest scores.
 
    We can compare results with the Puget Sound Regional Household Travel Survey. 
    However, keep in mind that survey techniques incorporate behavior biases, 
    such as those based on income, job status, etc. 
    But our universal basket of destinations is based on opportunity, 
    for which we do not want to start with different basket for different people. 
    This does not preclude the use of weighting coefficients that 
    could tune baskets for different income levels or types of households. 

    construct the basket for each blockgroup, calculate the proximity ratio,
    and compare it with sample results from the PSRC survey
    """
    # why global variables? 
    # global df_sample 
    # global df_destinations

    df_destinations = input_destinations
    # filter to match basket parameters based on rank (distance from destination)
    for i in range(len(CLASS_LIST)):
        df_destinations = df_destinations[(df_destinations['class'] != CLASS_LIST[i]) | (df_destinations['rank'] <= testArray[i])]
     
    # aggregate block group trips
    # proximity ration = trips under 2 miles vs trips between 2 and 10 miles; rows with zero denominators are removed
    df_destinations['dist_under_2'] = np.where(df_destinations['distance'] < 2.0, 1,0)
    df_destinations['dist_2_to_10'] = np.where((df_destinations['distance'] >= 2) & (df_destinations['distance'] < 10.0), 1, 0)
    df_blockgroup = df_destinations.groupby(['origin'], as_index=False).agg({'dist_under_2':sum,'dist_2_to_10':sum})
    df_blockgroup = df_blockgroup[df_blockgroup['dist_2_to_10'] != 0]   
    df_blockgroup['proximity_ratio_test'] = df_blockgroup['dist_under_2'] / df_blockgroup['dist_2_to_10']
 
    # merge with evaluation file
    df_merged = pd.merge(left=df_blockgroup, right=df_sample, how='left', left_on='origin', right_on='bg_origin')
    df_merged = df_merged.dropna()
    
    # evaluate results for this test array
    target = df_merged['proximity_ratio']
    predictions = df_merged['proximity_ratio_test']
    mse = mean_squared_error(target, predictions)

    return (mse)


# to test the function using two test arrays
"""
df_sample = pd.read_csv(os.path.join(DATADIR, 'Proximity_Ratio.csv')) 
input_destinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv'))
testArray1 = [0, 8, 0, 0, 0, 0, 0, 0, 0, 3]
testArray2 = [2, 11, 3, 2, 2, 2, 1, 0, 1, 2]
print(distilleBasketTest(testArray1))
print(distilleBasketTest(testArray2))
"""


## Brute force function to evaluate all combinations. There are 200,000 possible combinations.

df_sample = pd.read_csv(os.path.join(DATADIR, 'Proximity_Ratio.csv')) 
input_destinations = pd.read_csv(os.path.join(DATADIR, 'GoogleMatrix_Places_Dist.csv')) 

df_basket_combinations = pd.DataFrame()

#sizeLimit = 25
size_limit = int(input("Enter sizeLimit(I strongly suggest 40 or 41): "))


# Define parameter domain
AA = [0, 1, 2, 3, 4] # urban village
BB = [8, 9, 10, 11, 12, 13] # citywide destination
A = [0, 1, 2, 3] # destination park
B = [0, 1, 2, 3] # supermarket
C = [0, 1, 2, 3] # library
D = [0, 1, 2, 3] # hospital
E = [0, 1, 2, 3] # pharmacy
F = [0, 1, 2, 3] # post office
G = [0, 1, 2, 3] # school
H = [0, 1, 2, 3] # cafe

count_combinations = 0
score = []
parameters = []

for x in itertools.product(AA, BB, A, B, C, D, E, F, G, H):
    
    count_variables = 0

    for item in x:
        count_variables += item
    
    if count_variables == size_limit: # valid combination
        parameters.append(x)
        score.append(distill_basket_test(x))
        count_combinations += 1

print("Combinations: " + str(count_combinations))
print("Parameters (arrays of ranks): " + str(parameters))
print("Score: ", score)
