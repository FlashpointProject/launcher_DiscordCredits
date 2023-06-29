import sys
import csv
import json

if len(sys.argv) != 3:
	print('Usage: python csvImport.py credits.json credits.csv')
	sys.exit()
json_filename = sys.argv[1]
csv_filename = sys.argv[2]

fields = ['id', 'title', 'note']

with open(json_filename, 'r') as f:
	credits_json = json.load(f)
	profiles = credits_json['profiles']

with open(csv_filename, 'r', encoding='utf-8') as csvfile: 
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		rowID = int(row['id'])
		if rowID == 0:
			profileIndex = next((i for i, profile in enumerate(profiles) 
								 if profile['id'] == 0 and profile['title'] == row['title']), None)
		else:
			profileIndex = next((i for i, profile in enumerate(profiles) if profile['id'] == rowID), None)
		if profileIndex is None:
			print('Failed to import row:', str(row))
		else:
			profile = profiles[profileIndex]
			if row['title'] and (profile['title'] != row['title']):
				print('Updated preferred name:', profile['title'], '=>', row['title'])
				profile['title'] = row['title']
				profile['keepTitle'] = True
			if row['note'] and (profile['note'] != row['note']):
				print('Updated note for', profile['title'], ":", row['note'])
				profile['note'] = row['note']
			profiles[profileIndex] = profile

credits_json['profiles'] = profiles
with open(json_filename, 'w') as f:
	json.dump(credits_json, f, indent=2)
print(f'Finished importing data from {csv_filename} to {json_filename}')