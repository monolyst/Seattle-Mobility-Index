import numpy as np
import pandas as pd
import sqlite3
import sys
import re

def convert_csv(path, dbfile):
    """
    Path is entered as a command-line argument.
    """

    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()

    table_name = re.search(r'([\w]+)[.csv]', path).group(1)
    
    df = pd.read_csv(path)
    keys = (pd.read_csv(path, nrows=1).columns).tolist()

    df.to_sql(table_name, conn, schema=None, if_exists='fail')

    conn.commit()
    conn.close()

def main(argv):
    path = "../seamo/data/raw/" + str(sys.argv[1]) + ".csv"
    dbfile = str(sys.argv[2]) + ".sqlite3"
    convert_csv(path, dbfile)

if __name__ == "__main__":
    main(sys.argv[1:])