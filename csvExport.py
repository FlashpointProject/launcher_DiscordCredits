import sys
import csv
import json

if len(sys.argv) != 3:
	print('Usage: python csvExport.py credits.json credits.csv')
	sys.exit()
json_filename = sys.argv[1]
csv_filename = sys.argv[2]

fields = ['id', 'title', 'note']

with open(json_filename, 'r') as f:
	credits_json = json.load(f)
	profiles = credits_json['profiles']

with open(csv_filename, 'w', encoding='utf-8', newline='') as csvfile: 
	csvwriter = csv.DictWriter(csvfile, fields, extrasaction='ignore')
	csvwriter.writeheader()
	csvwriter.writerows(profiles)

print(f'Finished exporting data from {json_filename} to {csv_filename}')