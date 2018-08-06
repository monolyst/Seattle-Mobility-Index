import init
import sqlite3
import sys
import re
import os
import sqlalchemy
import constants as cn
import pickle
import pandas as pd


def df_to_sql(df, table_name, db_filename):
    db_file = os.path.join(cn.DB_DIR, str(db_filename) + '.db')
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, schema=None, if_exists='fail', index=False)
    conn.commit()
    conn.close()


def sql_to_df(db_name):
    db_file = os.path.join(cn.DB_DIR, db_name + '.db')
    conn = sqlite3.connect(db_file)
    df = read_sql_table(db_file, conn)
    conn.commit()
    conn.close()
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
    df[key] = df.apply(lambda x: x[key].rstrip('.0'), axis=1)
    return df