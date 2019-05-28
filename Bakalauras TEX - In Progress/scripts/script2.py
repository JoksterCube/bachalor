import csv
import numpy as np
import pandas as pd
import urllib.parse as up
import urllib.request as ur
import json
new_file_3G_csv = 'Data/Processed/measurements-3G.csv'
new_file_LTE_csv = 'Data/Processed/measurements-LTE.csv'
new_file_WiMAX_csv = 'Data/Processed/measurements-WiMAX.csv'
more_data_file_3G_csv = 'Data/Processed/more-measurements-3G.csv'
more_data_file_LTE_csv = 'Data/Processed/more-measurements-LTE.csv'
more_data_file_WiMAX_csv = 'Data/Processed/more-measurements-WiMAX.csv'
token = "XPlYEbsLssXaMRcPolV9txdQyrZ0LrOTA5Hn9bq6SW7jvnb92rsKQZbx2augAEpL"
main_url = "https://api.jawg.io/elevations?"
request_step = 100
round_digits = 1
new_X_3G = []
new_X_LTE = []
new_X_WiMAX = []

read_3G = pd.read_csv(new_file_3G_csv)
X_3G = np.array(read_3G)
y_3G = np.array(read_3G.columns)
lat_3G = np.where(y_3G == 'latitude')[0][0]
long_3G = np.where(y_3G == 'longitude')[0][0]
lats_3G = X_3G[0:,lat_3G]
longs_3G = X_3G[0:,long_3G]
prev_r = 0
len_3G = len(X_3G)
locations_3G = []
for r in range(request_step, len_3G + request_step, request_step):
    locs_3G = []
    for i in range(prev_r, r):
		if i >= len_3G:
			break
        locs_3G.append(str(lats_3G[i]) + ',' +  str(longs_3G[i]))
    prev_r = r
    
    locations_3G.append("|".join(locs_3G))
elevation_3G = np.array([])
for loc in locations_3G:
    params = {'locations': loc, 'access-token' : token}
    full_url = main_url + up.urlencode(params)
    request = ur.urlopen(full_url)
    contents = request.read()
    request.close()
    jdata = json.loads(contents)
    el = np.array([j['elevation'] for j in jdata])
    elevation_3G = np.concatenate((elevation_3G, el))
new_X_3G = []
for i in range(len_3G):
    item = X_3G[i]
    new_item = []
    new_item.append(round(item[lat_3G], round_digits))
    new_item.append(round(item[long_3G], round_digits))
    new_item.append(elevation_3G[i])
    new_item.append(round(elevation_3G[i] / 10, 0) * 10)
    complete_item = np.append(np.array(item), np.array(new_item))
    new_X_3G.append(complete_item)
new_X_3G = np.array(new_X_3G)
with open(more_data_file_3G_csv, mode='w') as new_3G_csv_file:
    writer_3G = csv.writer(new_3G_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer_3G.writerow(['year', 'latitude', 'longitude', 'altitude', 'lat_1', 'long_1', 'alt_10', 'provider', 'cell_id', 'rssi', 'technology', 'speed'])
    for item in new_X_3G:
        writer_3G.writerow([item[0], item[1], item[2], item[10], item[8], item[9], int(item[11]), item[3], item[4], item[5], item[6], item[7]])

read_LTE = pd.read_csv(new_file_LTE_csv)
X_LTE = np.array(read_LTE)
y_LTE = np.array(read_LTE.columns)
lat_LTE = np.where(y_LTE == 'latitude')[0][0]
long_LTE = np.where(y_LTE == 'longitude')[0][0]
lats_LTE = X_LTE[0:,lat_LTE]
longs_LTE = X_LTE[0:,long_LTE]
prev_r = 0
len_LTE = len(X_LTE)
locations_LTE = []
for r in range(request_step, len_LTE + request_step, request_step):
    locs_LTE = []
    for i in range(prev_r, r):
		if i >= len_LTE:
			break
        locs_LTE.append(str(lats_LTE[i]) + ',' +  str(longs_LTE[i]))
    prev_r = r 
    locations_LTE.append("|".join(locs_LTE))
elevation_LTE = np.array([])
for loc in locations_LTE:
    params = {'locations': loc, 'access-token' : token}
    full_url = main_url + up.urlencode(params)
    request = ur.urlopen(full_url)
    contents = request.read()
    request.close()
    jdata = json.loads(contents)
    el = np.array([j['elevation'] for j in jdata])
    elevation_LTE = np.concatenate((elevation_LTE, el))
new_X_LTE = []
for i in range(len_LTE):
    item = X_LTE[i]
    new_item = []
    new_item.append(round(item[lat_LTE], round_digits))
    new_item.append(round(item[long_LTE], round_digits))
    new_item.append(elevation_LTE[i])
    new_item.append(round(elevation_LTE[i] / 10, 0) * 10)
    complete_item = np.append(np.array(item), np.array(new_item))
    new_X_LTE.append(complete_item)
new_X_LTE = np.array(new_X_LTE)
with open(more_data_file_LTE_csv, mode='w') as new_LTE_csv_file:
    writer_LTE = csv.writer(new_LTE_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer_LTE.writerow(['year', 'latitude', 'longitude','altitude', 'lat_1', 'long_1', 'alt_10', 'provider', 'cell_id', 'rssi', 'rsrp', 'speed'])
    for item in new_X_LTE:
        writer_LTE.writerow([item[0], item[1], item[2], item[10], item[8], item[9], int(item[11]), item[3], item[4], item[5], item[6], item[7]])

read_WiMAX = pd.read_csv(new_file_WiMAX_csv)
X_WiMAX = np.array(read_WiMAX)
y_WiMAX = np.array(read_WiMAX.columns)
lat_WiMAX = np.where(y_WiMAX == 'latitude')[0][0]
long_WiMAX = np.where(y_WiMAX == 'longitude')[0][0]
lats_WiMAX = X_WiMAX[0:,lat_WiMAX]
longs_WiMAX = X_WiMAX[0:,long_WiMAX]
prev_r = 0
len_WiMAX = len(X_WiMAX)
locations_WiMAX = []
for r in range(request_step, len_WiMAX + request_step, request_step):
    locs_WiMAX = []
    for i in range(prev_r, r):
		if i >= len_WiMAX:
			break
        locs_WiMAX.append(str(lats_WiMAX[i]) + ',' +  str(longs_WiMAX[i]))
    prev_r = r
    locations_WiMAX.append("|".join(locs_WiMAX))
elevation_WiMAX = np.array([])
for loc in locations_WiMAX:
    params = {'locations': loc, 'access-token' : token}
    full_url = main_url + up.urlencode(params)
    request = ur.urlopen(full_url)
    contents = request.read()
    request.close()
    jdata = json.loads(contents)
    el = np.array([j['elevation'] for j in jdata])
    elevation_WiMAX = np.concatenate((elevation_WiMAX, el))
new_X_WiMAX = []
for i in range(len_WiMAX):
    item = X_WiMAX[i]
    new_item = []
    new_item.append(round(item[lat_WiMAX], round_digits))
    new_item.append(round(item[long_WiMAX], round_digits))
    new_item.append(elevation_WiMAX[i])
    new_item.append(round(elevation_WiMAX[i] / 10, 0) * 10)
    complete_item = np.append(np.array(item), np.array(new_item))
    new_X_WiMAX.append(complete_item)
new_X_WiMAX = np.array(new_X_WiMAX)
with open(more_data_file_WiMAX_csv, mode='w') as new_WiMAX_csv_file:
    writer_WiMAX = csv.writer(new_WiMAX_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer_WiMAX.writerow(['year', 'latitude', 'longitude', 'altitude', 'lat_1', 'long_1', 'alt_10', 'base_station_id', 'rssi', 'cinr', 'speed'])
    for item in new_X_WiMAX:
        writer_WiMAX.writerow([item[0], item[1], item[2], item[9], item[7], item[8], int(item[10]), item[3], item[4], item[5], item[6]])