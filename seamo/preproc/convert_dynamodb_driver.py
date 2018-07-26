import init
import pandas as pd
import convert_dynamodb
import data_accessor as daq
import constants as cn

driving = convert_dynamodb.ConvertDynamodbDriving()
car = driving.dataframe
driving.write_to_csv(car, cn.GOOGLE_DIST_MATRIX_OUT + '_driving')

transit = convert_dynamodb.ConvertDynamodbTransit()
train = transit.dataframe
transit.write_to_csv(train, cn.GOOGLE_DIST_MATRIX_OUT + '_transit')

biking = convert_dynamodb.ConvertDynamodbBiking()
bike = biking.dataframe
biking.write_to_csv(bike, cn.GOOGLE_DIST_MATRIX_OUT + '_biking')

walking = convert_dynamodb.ConvertDynamodbWalking()
walk = walking.dataframe
walking.write_to_csv(walk, cn.GOOGLE_DIST_MATRIX_OUT + '_walking')


df = pd.concat([car, train, bike, walk])
daq.write_to_csv(df, cn.GOOGLE_DIST_MATRIX_OUT + '.csv')
print('done')