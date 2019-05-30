#!/usr/bin/env python
# coding: utf-8
import csv
import numpy as np
import pandas as pd
def read_csv(file_name):
    read = pd.read_csv(file_name)
    X = np.array(read)
    labels = np.array(read.columns)
    return X, labels
def get_datetime_indexes(columns):
    dd = np.where(columns == 'date')[0][0]
    tt = np.where(columns == 'time')[0][0]
    return dd, tt  
def create_new_x(x, dd, tt):
    i = max(dd, tt)
    new_x = []
    for row in x:
        new_row = row.tolist()
        new_row.insert(i+1, row[dd][:4])
        new_row.insert(i+2, row[tt][:2])
        new_x.append(new_row)
    new_x = np.array(new_x)
    return new_x
def create_new_l(l, dd, tt, yl, hl):
    i = max(dd, tt)
    new_l = l.tolist()
    new_l.insert(i+1, yl)
    new_l.insert(i+2, hl)
    new_l = np.array(new_l)
    return new_l
def write_csv(file_name, x, labels):
    with open(file_name, mode='w') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(labels)
        for row in x:
            writer.writerow(row)
def your_hour_change_file(file_name, new_file_name, year_label, hour_label):
    x, l = read_csv(file_name)
    dd, tt = get_datetime_indexes(l)
    new_x = create_new_x(x, dd, tt)
    new_l = create_new_l(l, dd,tt, year_label, hour_label)
    write_csv(new_file_name, new_x, new_l)
    print('Done')
file_3G_csv = 'Data/Processed/altitude-3G.csv'
file_LTE_csv = 'Data/Processed/altitude-LTE.csv'
file_WiMAX_csv = 'Data/Processed/altitude-WiMAX.csv'
new_file_3G_csv = 'Data/Processed/yh-3G.csv'
new_file_LTE_csv = 'Data/Processed/yh-LTE.csv'
new_file_WiMAX_csv = 'Data/Processed/yh-WiMAX.csv'
year_label = 'year'
hour_label = 'hour'
your_hour_change_file(file_3G_csv, new_file_3G_csv, year_label, hour_label)
your_hour_change_file(file_LTE_csv, new_file_LTE_csv, year_label, hour_label)
your_hour_change_file(file_WiMAX_csv, new_file_WiMAX_csv, year_label, hour_label)
