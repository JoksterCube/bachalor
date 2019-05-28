import csv
file_3G_csv = 'Data/Raw/Matavimai-3G.csv'
file_LTE_csv = 'Data/Raw/Matavimai-LTE.csv'
file_WiMAX_csv = 'Data/Raw/Matavimai-WiMAX.csv'
new_file_3G_csv = 'Data/Processed/measurements-3G.csv'
new_file_LTE_csv = 'Data/Processed/measurements-LTE.csv'
new_file_WiMAX_csv = 'Data/Processed/measurements-WiMAX.csv'

with open(new_file_3G_csv, mode='w') as new_3G_csv_file:
	writer_3G = csv.writer(new_3G_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer_3G.writerow(['year', 'latitude', 'longitude', 'provider', 'cell_id', 'rssi', 'technology', 'speed'])
	with open(file_3G_csv , mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			year = row['data ir laikas'][:4]
			latitude = row['platuma']
			longitude = row['ilguma']
			provider = row['operatorius']
			cell_id = row['celės id']
			rssi = row['rssi']
			technology = row['3G ryšio technologija']
			speed = row['sparta kbit/s']
			writer_3G.writerow([year, latitude, longitude, provider, cell_id, rssi, technology, speed])
			line_count += 1
		print(f'Processed {line_count} 3G CSV file lines.')
		
with open(new_file_LTE_csv, mode='w') as new_LTE_csv_file:
	writer_LTE = csv.writer(new_LTE_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer_LTE.writerow(['year', 'latitude', 'longitude', 'provider', 'cell_id', 'rssi', 'rsrp', 'speed'])
	with open(file_LTE_csv , mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			year = row['data ir laikas'][:4]
			latitude = row['platuma']
			longitude = row['ilguma']
			provider = row['operatorius']
			cell_id = row['celės id']
			rssi = row['rssi']
			rsrp = row['rsrp']
			speed = row['sparta kbit/s']
			writer_LTE.writerow([year, latitude, longitude, provider, cell_id, rssi, rsrp, speed])
			line_count += 1
		print(f'Processed {line_count} LTE CSV file lines.')
		
with open(new_file_WiMAX_csv, mode='w') as new_WiMAX_csv_file:
	writer_WiMAX = csv.writer(new_WiMAX_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer_WiMAX.writerow(['year', 'latitude', 'longitude', 'base_station_id', 'rssi', 'cinr', 'speed'])
	with open(file_WiMAX_csv , mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			year = row['data ir laikas'][:4]
			latitude = row['platuma']
			longitude = row['ilguma']
			base_station_id = row['bazinės stoties id']
			rssi = row['rssi']
			cinr = row['cinr']
			speed = row['sparta kbit/s']
			writer_WiMAX.writerow([year, latitude, longitude, base_station_id, rssi, cinr, speed])
			line_count += 1
		print(f'Processed {line_count} WiMAX CSV file lines.')