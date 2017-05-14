import os
import pandas as pd


# Reads in all files and returns a list of file names in order
def read_files(which='_prices.csv', folder='prices'):
    files = [f for f in os.listdir(folder) if which in f]
    files.sort()
    return files


def read_all(which='_prices.csv', folder='prices'):
    files = read_files()
    list_ = []
    for cf in files:
        df = pd.read_csv(os.path.join(folder, cf), index_col='times', parse_dates=True)
        list_.append(df)
    return pd.concat(list_).sort_index()


# Define a day between 1 and 50
def read_day(day=1, which='_prices.csv', folder='prices'):
    list_ = []
    files = [f for f in os.listdir(folder) if which in f]
    files.sort()
    cf = files[day - 1]
    df = pd.read_csv(os.path.join(folder, cf), index_col='times', parse_dates=True)
    list_.append(df)
    return pd.concat(list_).sort_index()


def read_from_till(start, end):
    days = []
    for i in range(start, end):
        day = read_day(i)
        days.append(day)
    return days
