import init
import os
import boto3
import pandas as pd

# Get AWS service resource.
   dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
   aws_access_key_id = os.environ['aws_access_key_id']
   aws_secret_access_key = os.environ['aws_secret_access_key'] 

   table = dynamodb.Table('seamo-' +MODE)