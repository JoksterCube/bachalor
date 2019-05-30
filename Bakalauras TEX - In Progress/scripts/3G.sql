#Pradiniai duomenys
IMPORT FROM CSV FILE '~/Data/Raw/raw-3G.csv' INTO r3G(date string, time string, latitude double, longitude double, provider string, cell_id string, rssi double, technology string, speed double);
SELECT * FROM
	DIFF
		(SPLIT (
			SELECT *, percentile(speed) as pct FROM r3G)
		WHERE pct > 0.99)
	ON *
	WITH MIN SUPPORT 0.01 MIN RATIO 3.0
	COMPARE BY risk_ratio(COUNT(*))
	ORDER BY support
	INTO OUTFILE 'Output Data/3G/raw-3G.csv' FIELDS TERMINATED BY ',';
# Papildyti aukscio ir suapvalintomis reiksmemis duomenys
IMPORT FROM CSV FILE '~/Data/Processed/altitude-3G.csv' INTO a3G(date string, time string, latitude double, longitude double, altitude double, lat string, lng string, alt string, provider string, cell_id string, rssi double, technology string, speed double);
SELECT * FROM
	DIFF
		(SPLIT (
			SELECT *, percentile(speed) as pct FROM a3G)
		WHERE pct > 0.99)
	ON *
	WITH MIN SUPPORT 0.01 MIN RATIO 3.0
	COMPARE BY risk_ratio(COUNT(*))
	ORDER BY support
	INTO OUTFILE 'Output Data/3G/altitude-3G.csv' FIELDS TERMINATED BY ',';
# Papildyti metu ir valandu laukais duomenys
IMPORT FROM CSV FILE '~/Data/Processed/yh-3G.csv' INTO y3G(date string, time string, year string, hour string, latitude double, longitude double, altitude double, lat string, lng string, alt string, provider string, cell_id string, rssi double, technology string, speed double);
SELECT * FROM
	DIFF
		(SPLIT (
			SELECT *, percentile(speed) as pct FROM y3G)
		WHERE pct > 0.99)
	ON *
	WITH MIN SUPPORT 0.01 MIN RATIO 3.0
	COMPARE BY risk_ratio(COUNT(*))
	ORDER BY support
	INTO OUTFILE 'Output Data/3G/yh-3G.csv' FIELDS TERMINATED BY ',';