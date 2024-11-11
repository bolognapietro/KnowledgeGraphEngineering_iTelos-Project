import os
import csv

def datitrentino():
    input_folder = 'Phase 2 - Information Gathering/data/raw/dati.trentino.it/csv'
    output_file = 'Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/fixed_csv'
    
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith('.csv'):
            with open(os.path.join(input_folder, filename), 'r') as infile:
                reader = csv.reader(infile, delimiter=';')
                header = next(reader)
                output_path = os.path.join(output_file, filename)
                with open(output_path, 'w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    header_written = False
                    if not header_written:
                        writer.writerow(header)
                        header_written = True
                    row_count = 0
                    for row in reader:
                        if '2024' in ''.join(row):
                            writer.writerow(row)
                            row_count += 1
                if row_count < 2:
                    os.remove(output_path)


datitrentino()
