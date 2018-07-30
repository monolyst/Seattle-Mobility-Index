import init
import sqlite3
import sys
import re
import os
import sqlalchemy
import constants as cn


def df_to_sql(df, table_name):
    self.table_name = table_name
    db_file = os.path.join(cn.DB_DIR, str(self.table_name) + '.db')
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, schema=None, if_exists='fail', index=False)
    conn.commit()
    conn.close()


def sql_to_df(db_name=cn.GOOGLE_DIST_MATRIX_OUT):
    db_file = os.path.join(cn.DB_DIR, db_name + '.db')
    conn = sqlite3.connect(db_file)
    df = read_sql_table(db_file, conn)
    conn.commit()
    conn.close()
    return df


def write_to_csv(df, output_file, processed_dir=cn.CSV_DIR):
    df.to_csv(os.path.join(processed_dir, output_file), index=False)