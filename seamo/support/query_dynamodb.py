import init
import os
import boto3
import pandas as pd

# Get AWS service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key'] 

df_names = ['driving':car, 'transit':transit, 'biking':bike, 'walking':walk]
for mode in ['driving', 'transit', 'biking', 'walking']:
    table = dynamodb.Table('seamo-' +mode)
    # process table for specific mode into pandas dataframe
    df_names[mode] = pd.DataFrame(table)
    

# use df_to_sql to convert to sqlite3 db
def df_to_sql(df, table_name):
    table_name = table_name
    db_file = os.path.join(cn.DB_DIR, str(table_name) + '.db')
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, schema=None, if_exists='fail', index=False)
    conn.commit()
    conn.close()

df_to_sql(car, 'driving')
df_to_sql(transit, 'transit')
df_to_sql(bike, 'biking')
df_to_sql(walk, 'walking')