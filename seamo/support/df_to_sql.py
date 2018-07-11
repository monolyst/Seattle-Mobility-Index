import __init__
import sqlite3
import sys
import re
import os
import sqlalchemy
import constants as cn

def df_to_sql(df, table_name):
    db_file = os.path.join(cn.DB_DIR, str(table_name) + '.db')
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, schema=None, if_exists='fail', index=False)
    conn.commit()
    conn.close()