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
def get_col_indexes(columns):
    latitude = np.where(columns == 'latitude')[0][0]
    longitude = np.where(columns == 'longitude')[0][0]
    altitude = np.where(columns == 'altitude')[0][0]
    lat = np.where(columns == 'lat')[0][0]
    lng = np.where(columns == 'lng')[0][0]
    alt = np.where(columns == 'alt')[0][0]
    return latitude, longitude, altitude, lat, lng, alt
def change_x(x, latitude, longitude, altitude, lat, lng, alt, rd, ra):
    for i in range(len(x)):
        item = x[i]
        item[lat] = round(item[latitude], rd)
        item[lng] = round(item[longitude], rd)
        item[alt] = round(round(item[altitude] / 10 * ra) * 10 / ra, 2)
def name_new_file(file_name, rd, ra):
    return file_name.format(rd, ra)
def write_csv(file_name, x, labels):
    with open(file_name, mode='w') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(labels)
        for row in x:
            writer.writerow(row)
def perform_all_tests(file_name, new_file_name, rdt, rat):
    x, l = read_csv(file_name)
    latitude, longitude, altitude, lat, lng, alt = get_col_indexes(l)
    for rd in rdt:
        for ra in rat:
            full_name = name_new_file(new_file_name, rd, ra)
            change_x(x, latitude, longitude, altitude, lat, lng, alt, rd, ra)
            write_csv(full_name, x, l)
            print(f'{rd}{ra} Done.')
        print('Cycle.')
    print('All done.')
file_3G_csv = 'Data/Processed/yh-3G.csv'
file_LTE_csv = 'Data/Processed/yh-LTE.csv'
file_WiMAX_csv = 'Data/Processed/yh-WiMAX.csv'
new_file_3G_csv = 'Data/Processed/3G/{}{}-3G.csv'
new_file_LTE_csv = 'Data/Processed/LTE/{}{}-LTE.csv'
new_file_WiMAX_csv = 'Data/Processed/WiMAX/{}{}-WiMAX.csv'
round_digit_tests = range(3+1)
round_altitude_tests = range(1, 5+1)
perform_all_tests(file_3G_csv, new_file_3G_csv, round_digit_tests, round_altitude_tests)
perform_all_tests(file_LTE_csv, new_file_LTE_csv, round_digit_tests, round_altitude_tests)
perform_all_tests(file_WiMAX_csv, new_file_WiMAX_csv, round_digit_tests, round_altitude_tests)
