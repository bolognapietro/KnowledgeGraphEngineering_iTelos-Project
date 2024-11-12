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
input_path = "Phase 2 - Information Gathering/data/raw/overpass-turbo.eu/csv"
output_path = "Phase 2 - Information Gathering/data/cleaned/overpass-turbo.eu/csv"
copy_files(input_path, output_path)
