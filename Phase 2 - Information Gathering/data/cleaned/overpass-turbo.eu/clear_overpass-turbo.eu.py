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

# Copy files from raw to cleaned
# input_path = "Phase 2 - Information Gathering/data/raw/overpass-turbo.eu/csv"
output_path = "Phase 2 - Information Gathering/data/cleaned/overpass-turbo.eu/csv"
# copy_files(input_path, output_path)

def count_volleyball_lit_rows(csv_dir):
    count_volleyball = 0
    count_lit = 0
    count_covered = 0
    count_surface = 0
    for filename in os.listdir(csv_dir):
        file_path = os.path.join(csv_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "volleyball" in row.get('sport'):
                        count_volleyball += 1
                        if 'lit' in row and row.get('lit') == 'True' or row.get('lit') == 'False':
                            count_lit += 1
                        if 'covered' in row and row.get('covered') == 'True' or row.get('covered') == 'False':
                            count_covered += 1
                        if 'surface' in row and row.get('surface'):
                            count_surface += 1
    return count_volleyball, count_lit, count_covered, count_surface

volleyball, lit, covered, surface = count_volleyball_lit_rows(output_path)
print(f"Number of rows with 'volleyball': {volleyball}")
print(f"Number of rows with 'volleyball' and attribute 'lit': {lit}")
print(f"Number of rows with 'volleyball' and attribute 'covered': {covered}")
print(f"Number of rows with 'volleyball' and attribute 'surface': {surface}")
