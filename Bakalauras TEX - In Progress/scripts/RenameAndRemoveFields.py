#!/usr/bin/env python
# coding: utf-8
import csv
import numpy as np
import pandas as pd
file_3G_csv = 'Data/Raw/Matavimai-3G.csv'
file_LTE_csv = 'Data/Raw/Matavimai-LTE.csv'
file_WiMAX_csv = 'Data/Raw/Matavimai-WiMAX.csv'
new_file_3G_csv = 'Data/Raw/raw-3G.csv'
new_file_LTE_csv = 'Data/Raw/raw-LTE.csv'
new_file_WiMAX_csv = 'Data/Raw/raw-WiMAX.csv'
new_3G_labels = ['date', 'time', 'latitude', 'longitude', 'provider', 'cell_id', 'rssi', 'technology', 'speed']
new_LTE_labels = ['date', 'time', 'latitude', 'longitude', 'provider', 'cell_id', 'rssi', 'speed']
new_WiMAX_labels = ['date', 'time', 'latitude', 'longitude', 'base_station_id', 'rssi', 'speed']
useful_3G_cols = [0, 1, 2, 3, 4, 5, 7, 8]
useful_LTE_cols = [0, 1, 2, 3, 4, 5, 10]
useful_WiMAX_cols = [0, 1, 2, 4, 5, 8]
def read_csv(file_name):
    read = pd.read_csv(file_name)
    x = np.array(read)
    return x
def create_new_file(file_name, x, useful_cols, new_labels):
    line_count = 0
    with open(file_name, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(new_labels)
        line_count = 0
        for row in x:
            useful_row = [row[i] for i in useful_cols]
            date, time = useful_row[0].split()
            useful_row[0] = date
            useful_row.insert(1, time)
            writer.writerow(useful_row)
            line_count += 1
    print(f'Processed {line_count} lines.')
    return line_count
def read_and_write(file_name, new_file_name, new_labels, useful_cols):
    x = read_csv(file_name)
    create_new_file(new_file_name, x, useful_cols, new_labels)
    print('Done')
read_and_write(file_3G_csv, new_file_3G_csv, new_3G_labels, useful_3G_cols)
read_and_write(file_LTE_csv, new_file_LTE_csv, new_LTE_labels, useful_LTE_cols)
read_and_write(file_WiMAX_csv, new_file_WiMAX_csv, new_WiMAX_labels, useful_WiMAX_cols)
