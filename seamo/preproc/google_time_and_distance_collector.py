# coding: utf-8
"""
Google Time and Distance Collector
 
This script accesses the Google Distance Matrix API to download distance
and travel times, given a datafile that contains origins and destinations.

The script is intended to be run in AWS Lambda using only Python native
libraries. Environmental variables for AWS services and the Google API
are required.

The data are saved to the AWS DynamoDB table "seamo".

We are implementing a Cloudwatch trigger with the cron script: 
cron(0 3-16 * * ? *), which has been adjusted for the Los_Angeles time zone
"""

# Libraries for API ETL
import json
import os
from urllib.request import Request, urlopen
import csv
from datetime import datetime
from dateutil import tz

# Libraries for AWS services
import boto3
import decimal

# API constants
DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
UNITS = 'imperial'
MODE = 'driving'


API_KEY = os.environ['API_KEY']

def lambda_handler(event, context):
    # TODO implement
    return 'Hello from Lambda'
    
# Get AWS service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
aws_access_key_id = os.environ['aws_access_key_id'] 
aws_secret_access_key = os.environ['aws_secret_access_key'] 

table = dynamodb.Table('seamo')

# Load trip attributes filter
f = open('./data/GoogleMatrix_Trips_In.csv')
csv_f = csv.reader(f)

# Access the Google Matrix API
for row in csv_f:
    
    origin = str(row[4]) + "," + str(row[5])
    destination = str(row[2]) + "," + str(row[3])
    
    url = DIST_MATRIX_URL +\
              'units={0}'.format(UNITS) +\
              '&mode={0}'.format(MODE) +\
              '&origins={0}'.format(origin) +\
              '&destinations={0}'.format(destination) +\
              "&key={0}".format(API_KEY)
    
    request = Request(url)
    try: 
        response = urlopen(request).read()
    except:
        raise Exception("Couldn't open link.")  

    data = json.loads(response)
    
    if data['status'] != 'OK':
        message = data['error_message']
        raise Exception(message)
        
        # Going to make a SeamoError type.
    else:
        elements = data['rows'][0]['elements']
        element = elements[0]
                
        if element['status'] == 'OK':
            distance = str(float(element['distance']['value'])/1609)
            if 'fare' in element:
                fare = element['fare']['value']
            
            if 'duration_in_traffic' in element:
                duration_in_traffic = str(float(element['duration_in_traffic']['value'])/60)
            
            duration = str(float(element['duration']['value'])/60)
            status = element['status']
            mode = MODE

            # convert from UTC to local time zone
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('America/Los_Angeles')
            utc = datetime.utcnow()
            utc = utc.replace(tzinfo=from_zone)
            local = utc.astimezone(to_zone)
            departure_time = str(local)
            tripID = "{0}++{1}".format(row[0],departure_time) 


            # save to DynamoDB

            if 'fare' in element:        
                response = table.put_item(
                    Item={
                        'tripID': tripID,
                        'mode': mode,
                        'fare': decimal.Decimal(str(fare)),
                        'duration': decimal.Decimal(str(duration)),
                        'distance': decimal.Decimal(str(distance)),
                        'departure_time': departure_time,
                        'status': status
                        }         
                )
    
            if 'duration_in_traffic' in element:        
                response = table.put_item(
                    Item={
                        'tripID': tripID,
                        'mode': mode,
                        'duration_in_traffic': decimal.Decimal(str(duration_in_traffic)),
                        'duration': decimal.Decimal(str(duration)),
                        'distance': decimal.Decimal(str(distance)),
                        'departure_time': departure_time,
                        'status': status
                        }         
                )

                
            if ('duration_in_traffic' not in element) & ('fare' not in element):        
                response = table.put_item(
                    Item={
                        'tripID': tripID,
                        'mode': mode,
                        'duration': decimal.Decimal(str(duration)),
                        'distance': decimal.Decimal(str(distance)),
                        'departure_time': departure_time,
                        'status': status
                        }         
                )