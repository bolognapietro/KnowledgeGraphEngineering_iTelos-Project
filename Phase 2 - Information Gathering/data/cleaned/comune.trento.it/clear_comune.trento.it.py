import os
import shutil

def copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dest_file)

    
input_path = "Phase 2 - Information Gathering/data/raw/comune.trento.it/csv"
output_path = "Phase 2 - Information Gathering/data/cleaned/comune.trento.it/csv"