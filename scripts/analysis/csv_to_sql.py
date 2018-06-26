"""
This module takes a data input as a csv file, and converts it to
a sqlite3 dbfile.
"""

import pandas as pd
import sqlite3
import sys
import re
import os


def convert_csv(path, dbfile):
    """
    Path is entered as a command-line argument.
    """

    conn = sqlite3.connect(dbfile)
    # cur = conn.cursor()

    table_name = re.search(r'([\w]+)[.csv]', path).group(1)
    csv_file = pd.read_csv(path)
    csv_file.to_sql(table_name, conn, schema=None, if_exists='fail')

    conn.commit()
    conn.close()


def main(argv):
    """
    Main function for conversion module.
    input argv is from command line.
    """

    data_path = "../seamo/data/"
    path = os.path.join(data_path + "raw/", str(sys.argv[1]) + ".csv")
    dbfile = os.path.join(data_path + "processed/", str(sys.argv[2])
        + ".sqlite3")
    convert_csv(path, dbfile)


if __name__ == "__main__":
    main(sys.argv[1:])
