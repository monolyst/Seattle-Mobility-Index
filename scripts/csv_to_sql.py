import numpy as np
import pandas as pd
import sqlite3
import sys

def convert_csv(path, dbfile):
    """
    Path is entered as a command-line argument.
    """

    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    

    df = pd.read_csv(path)
    keys = (pd.read_csv(path, nrows=1).columns).tolist()
    print(keys)

    cur.execute("CREATE TABLE data keys")
    # cur.exectutemany("INSERT INTO data (col1, col2) VALUES (?, ?);", to_db)
    #assuming that the header will contain information about the table title

    conn.commit()
    conn.close()

def main(argv):
    path = str(sys.argv[1])
    dbfile = str(sys.argv[2]) + ".sqlite3"
    convert_csv(path, dbfile)

if __name__ == "__main__":
    main(sys.argv[1:])