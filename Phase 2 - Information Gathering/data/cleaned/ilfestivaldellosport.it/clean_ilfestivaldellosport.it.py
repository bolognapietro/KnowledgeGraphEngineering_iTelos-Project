import os
import shutil
import csv

def copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dest_file)

    for filename in os.listdir(dest_dir):
        file_path = os.path.join(dest_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                content = file.read()
            with open(file_path, mode='w', encoding='utf-8') as file:
                file.write(content)

def rename_headers(directory):
    headers = {}
    headers_dict = {
        "date": "startDate",
    }
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers[filename] = next(reader)
                new_headers = [headers_dict.get(header, header) for header in headers[filename]]
                rows = list(reader)
                with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(new_headers)
                    writer.writerows(rows)

def edit_guest(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                rows = list(reader)
                
            guest_index = headers.index('guests') if 'guests' in headers else None
            if guest_index is not None:
                for row in rows:
                    row[guest_index] = row[guest_index].strip("[]").replace("'", "")
                    
            with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)


# Copy files from raw to cleaned
input_path = "Phase 2 - Information Gathering/data/raw/ilfestivaldellosport.it/csv"
output_path = "Phase 2 - Information Gathering/data/cleaned/ilfestivaldellosport.it/csv"
copy_files(input_path, output_path)

# Get headers from files
rename_headers(output_path)

# Edit guest column
edit_guest(output_path)

def split_location(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                rows = list(reader)
                
            location_index = headers.index('location') if 'location' in headers else None
            if location_index is not None:
                headers.extend(['address', 'municipality'])
                for row in rows:
                    location = eval(row[location_index])
                    address = f"{location['name']}, {location['address'].split(',')[0]}"
                    municipality = location['address'].split(',')[-1].strip()
                    row.extend([address, municipality])
                headers.remove('location')
                for row in rows:
                    row.pop(location_index)
                    
            with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)

# Split location column into address and municipality
split_location(output_path)