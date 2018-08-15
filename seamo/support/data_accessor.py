import init
import sqlite3
import sys
import re
import os
import sqlalchemy
import constants as cn
import pickle
import pandas as pd
from dateutil import parser


def df_to_sql(df, table_name, db_name, dtype=None, schema=None, processed_dir=cn.DB_DIR):
    db_file = os.path.join(processed_dir, str(db_name) + '.db')
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, schema=schema, if_exists='fail', index=False)
    conn.commit()
    conn.close()

def execute_query(queries, db_name, processed_dir=cn.DB_DIR):
    db_file = os.path.join(processed_dir, db_name + '.db')
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    if type(queries) is list:
        for query in queries:
            cur.execute(query)
    else:
        cur.execute(queries)
    conn.commit()
    conn.close()


def sql_to_df(query, db_name, processed_dir=cn.DB_DIR):
    db_file = os.path.join(processed_dir, db_name + '.db')
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn)
    conn.commit()
    conn.close()
    return df

def drop_table_if_exists(table_name):
    return cn.DROP_TABLE_IF_EXISTS + str(table_name) + ';'

def select_all_from(table_name):
    return cn.SELECT_ALL_FROM + str(table_name) + ';'


def csv_to_sql(csv_file, db_name, dtype=None, processed_dir=cn.CSV_DIR):
    table_name = re.search(r'([\w]+)[.csv]', csv_file).group(1)
    df = pd.read_csv(os.path.join(cn.CSV_DIR, csv_file), dtype=dtype)
    df_to_sql(df, table_name, db_name, dtype)


def query_goog_dist_mat_data(month_day, query=None, db_name=cn.GOOGLE_DIST_MATRIX_OUT):
    table_name = cn.GOOGLE_DIST_MATRIX_OUT + '_' + month_day
    if query is None:
        df = sql_to_df('select * from ' + table_name, db_name)
    else:
        df = sql_to_df(query, db_name)
    return df


def write_to_csv(df, output_file, processed_dir=cn.CSV_DIR):
    df.to_csv(os.path.join(processed_dir, output_file), index=False)



def make_pickle(processed_dir, df, pickle_name):
    with open(os.path.join(processed_dir, str(pickle_name)), 'wb') as pickle_file:
        pickle.dump(df, pickle_file)


def open_pickle(processed_dir, pickle_name):
    fname = processed_dir + str(pickle_name)
    return pickle.load(open(fname, 'rb'))

def read_csv_blockgroup_key(filepath, key):
    df = pd.read_csv(filepath, dtype={key: str})
    df[key] = df.apply(lambda x: x.key[:x.key.index('.')], axis=1)
    return df

def format_time(departure_time):
    return parser.parse(departure_time).replace(microsecond=0).replace(tzinfo=None)