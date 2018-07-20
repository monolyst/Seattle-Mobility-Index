import init
import sqlite3
import sys
import re
import os
import sqlalchemy
import constants as cn

class DataAccessor(object):
	def __init__(self):
		self.dataframe = None
		self.table_name = None

	def df_to_sql(self, df, table_name):
		self.table_name = table_name
	    db_file = os.path.join(cn.DB_DIR, str(self.table_name) + '.db')
	    conn = sqlite3.connect(db_file)
	    df.to_sql(table_name, conn, schema=None, if_exists='fail', index=False)
	    conn.commit()
	    conn.close()