import csv
import json

# Load CSV file
csv_filename = 'extra.csv'
csv_data = []
with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        if len(row) == 3:  # Ensure the row has id, title, and note
            csv_data.append(row)

# Load JSON file
json_filename = 'credits_new.json'
with open(json_filename, 'r') as json_file:
    json_data = json.load(json_file)

# Update JSON data with CSV values
for item in json_data['profiles']:
    item_id = item['id']
    for csv_row in csv_data:
        csv_id, csv_title, csv_note = csv_row
        if item_id != 0 and str(item_id) == csv_id:
            item['title'] = csv_title
            item['note'] = csv_note
            break  # Stop searching once a match is found

# Save updated JSON data
output_filename = 'updated_credits.json'
with open(output_filename, 'w') as output_file:
    json.dump(json_data, output_file, indent=4)

print("JSON file has been updated with CSV values.")
