import json
import csv
import os

def json_to_csv(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Process 'open_hours' and 'phone_number' fields if present
    for item in data:
        # Format 'open_hours' as a single string
        if 'open_hours' in item and isinstance(item['open_hours'], dict):
            item['open_hours'] = ', '.join(
                [f"{day}: {hours}" for day, hours in item['open_hours'].items()]
            )
        
        # Format 'phone_number' as a single string
        if 'phone_number' in item and isinstance(item['phone_number'], list):
            item['phone_number'] = ', '.join(item['phone_number'])
    
    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='') as csv_file:
        # Get the keys of the first dictionary as column headers
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header and data rows
        writer.writeheader()
        writer.writerows(data)
        
    print(f"CSV file has been saved to {csv_file_path}")

# Example usage
path = os.path.dirname(os.path.relpath(__file__))
json_folder_path = os.path.join(path, 'json')
csv_folder_path = os.path.join(path, 'csv_new')

# Create the CSV folder if it doesn't exist
os.makedirs(csv_folder_path, exist_ok=True)

# Iterate over all JSON files in the folder
for json_filename in os.listdir(json_folder_path):
    if json_filename.endswith('.json'):
        json_file_path = os.path.join(json_folder_path, json_filename)
        csv_filename = json_filename.replace('.json', '.csv')
        csv_file_path = os.path.join(csv_folder_path, csv_filename)
        json_to_csv(json_file_path, csv_file_path)

