#!/usr/bin/env python
# coding: utf-8
import csv
import numpy as np
import pandas as pd
import urllib.parse as up
import urllib.request as ur
import json
def read_csv(file_name):
    read = pd.read_csv(file_name)
    X = np.array(read)
    labels = np.array(read.columns)
    return X, labels
def get_coord_indexes(columns):
    lat = np.where(columns == 'latitude')[0][0]
    lng = np.where(columns == 'longitude')[0][0]
    return lat, lng  
def get_coords(x, lat_index, lng_index):
    lats = x[:,lat_index]
    lngs = x[:,lng_index]
    return lats, lngs
def create_formated_location_steps(lats, lngs, r_step):
    prev_r = 0
    l = len(lats)
    locations = []
    for r in range(r_step, l + r_step, r_step):
        locs = []
        for i in range(prev_r, r):
            if i >= l:
                break
            locs.append(str(lats[i]) + ',' +  str(lngs[i]))
        prev_r = r
        locations.append("|".join(locs))
    return locations
def get_elevations(locations, main_url, token):
    elevations = np.array([])
    a = 0
    for loc in locations:
        params = {'locations': loc, 'access-token' : token}
        full_url = main_url + up.urlencode(params)
        request = ur.urlopen(full_url)
        contents = request.read()
        request.close()
        jdata = json.loads(contents)
        el = np.array([j['elevation'] for j in jdata])
        elevations = np.concatenate((elevations, el))
        a += 1
        if a % 100 == 0:
            print(f'Processed altitude requests: {a}')
    return elevations
def create_new_X(x, lat, lng, els, c_round_digits, alt_round_parts=1):
    new_X = []
    for i in range(len(x)):
        item = x[i]
        new_item = []
        new_item.append(round(item[lat], c_round_digits))
        new_item.append(round(item[lng], c_round_digits))
        el = els[i]
        new_item.append(el)
        round_el = round(round(el / 10 * alt_round_parts) * 10 / alt_round_parts, 2)
        new_item.append(round_el)
        complete_item = np.append(np.array(item), np.array(new_item))
        new_X.append(complete_item)
    new_X = np.array(new_X)
    return new_X
def write_csv(file_name, x, labels, positinos):
    with open(file_name, mode='w') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(labels)
        for item in x:
            correct_pos_item = [item[p] for p in positions]
            writer.writerow(correct_pos_item)
def create_new_labels_and_positions(labels, lat, lng):
    positions = np.arange(len(labels)).tolist()
    labels_list = labels.tolist()
    last_i = len(labels)
    i = max(lat, lng)+1
    positions.insert(i, last_i+2)
    positions.insert(i+1, last_i)
    positions.insert(i+2, last_i+1)
    positions.insert(i+3, last_i+3)
    labels_list.insert(i, 'altitude')
    labels_list.insert(i+1, 'lat')
    labels_list.insert(i+2, 'lng')
    labels_list.insert(i+3, 'alt')
    labels_list = np.array(labels_list)
    return positions, labels_list
def create_new_csv_file(file_name, new_file_name, request_step, token, main_url, round_digits=2, round_altitude_parts=1):
    X, labels = read_csv(file_name)
    lat, lng = get_coord_indexes(labels)
    lats, lngs = get_coords(X, lat, lng)
    locations = create_formated_location_steps(lats, lngs, request_step)
    els = get_elevations(locations, main_url, token)
    new_X = create_new_X(X, lat, lng, els, round_digits, round_altitude_parts)
    positions, new_labels = create_new_labels_and_positions(labels, lat, lng)
    write_csv(new_file_name, new_X, new_labels, positions)
    print('Done')
file_3G_csv = 'Data/Raw/raw-3G.csv'
file_LTE_csv = 'Data/Raw/raw-LTE.csv'
file_WiMAX_csv = 'Data/Raw/raw-WiMAX.csv'
new_file_3G_csv = 'Data/Processed/altitude-11-3G.csv'
new_file_LTE_csv = 'Data/Processed/altitude-11-LTE.csv'
new_file_WiMAX_csv = 'Data/Processed/altitude-11-WiMAX.csv'
token = "nIXn7WWJTSeguG1aEuSioR2hM5PqAZUcRfGqCOV9RJvDwVJIYwDdDmwVDKvs5FYm"
main_url = "https://api.jawg.io/elevations?"
request_step = 100
round_digits = 1
round_altitude = 1
create_new_csv_file(file_3G_csv, new_file_3G_csv, request_step, token, main_url, round_digits, round_altitude)
create_new_csv_file(file_LTE_csv, new_file_LTE_csv, request_step, token, main_url, round_digits, round_altitude)
create_new_csv_file(file_WiMAX_csv, new_file_WiMAX_csv, request_step, token, main_url, round_digits, round_altitude)
