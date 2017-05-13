import os
import pandas as pd


def read_all(which='_prices.csv', folder='prices'):
    print("Reading all files which: " + which + " in folder: " + folder)
    list_ = []
    files = [f for f in os.listdir(folder) if which in f]
    files.sort()
    for cf in files:
        df = pd.read_csv(os.path.join(folder, cf), index_col='times', parse_dates=True)
        list_.append(df)
    return pd.concat(list_).sort_index()
