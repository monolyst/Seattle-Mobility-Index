# coding: utf-8

# In[3]:


import json
import os
import os.path
import boto3
import decimal
from pandas.io.json import json_normalize
import constants as cn


# In[4]:


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
    
# Scan call to DynamoDB
def scanDynamo(LastEvaluatedKey=None):

    # MODE = 'walking'
    MODE = 'driving'
    #MODE = 'driving'
    #MODE = 'bicycling'

    # Get AWS service resource.
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
    aws_access_key_id = os.environ['aws_access_key_id'], 
    aws_secret_access_key = os.environ['aws_secret_access_key'])

    table = dynamodb.Table('seamo-' + MODE)
    
    if (LastEvaluatedKey is None):
        response = table.scan()
    else:
        response = table.scan(
            ExclusiveStartKey = LastEvaluatedKey
        )
        
    print (response['ScannedCount'])
    #print (response)
    
    df_response = json_normalize(response,'Items')
    
    # save data to file
     # save data to file
    if os.path.isfile(os.path.join(cn.DYNAMODB_OUT_DIR, 'dynamo_out_' + MODE + '.csv')):
        df_response.to_csv(os.path.join(cn.DYNAMODB_OUT_DIR, 'dynamo_out_' + MODE + '.csv'), mode='a', header=False, index=False, encoding="utf-8")
    else:
        df_response.to_csv(os.path.join(cn.DYNAMODB_OUT_DIR, 'dynamo_out_' + MODE + '.csv'), mode='w', header=True, index=False, encoding="utf-8")
    
    # Call next page if available
    if 'LastEvaluatedKey' in response:
        scanDynamo(response['LastEvaluatedKey'])
    else:
        return     


# In[5]:


scanDynamo()