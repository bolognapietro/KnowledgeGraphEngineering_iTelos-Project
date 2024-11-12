import os
import csv
import pandas as pd
import re

# Takes raw data from raw/dati.trentino.it and cleans it by removing rows that do not contain the year 2024
def datitrentino_2024():
    input_folder = 'Phase 2 - Information Gathering/data/raw/dati.trentino.it/csv'
    output_file = 'Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv'
    
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith('.csv'):
            with open(os.path.join(input_folder, filename), 'r', encoding="utf-8") as infile:
                reader = csv.reader(infile, delimiter=';')
                header = next(reader)
                output_path = os.path.join(output_file, filename)
                with open(output_path, 'w', newline='', encoding="utf-8") as outfile:
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
                if row_count < 1:
                    os.remove(output_path)

# From the data of 2024, it removes the "&quot" from the csv files and then removes the files that are empty
def fix():
    input_path = "Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv"

    for filename in sorted(os.listdir(input_path)):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_path, filename)
            with open(file_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()
            
            with open(os.path.join(input_path, filename), 'w', encoding="utf-8") as file:
                for line in lines:
                    file.write(line.replace('&quot', ''))

# Fixes the row problem in the csv file 
def fix_row_problem(name):
    input_file = f"Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv/{name}.csv"
    
    with open(input_file, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        header = rows[0]
        header_len = len(header)
        
    with open(input_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in rows:
            if len(row) != header_len and "lon" in header:
                lon_index = header.index("lon")
                for i in range(1, header_len - len(row)+1):
                    row.insert(lon_index + i, '')
            writer.writerow(row)

# Prints the length of each row in the csv file
def row_len(name):
    input_file = f"Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv/{name}.csv"
    
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            print(f"Len row {i}: {len(row)}")


datitrentino_2024()
fix()

for filename in sorted(os.listdir("Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv")):
    if filename.endswith(".csv"):
        name = filename.replace(".csv", "")
        print(f"Processing {name}")
        fix_row_problem(name=name)

sports = ['Acrobatica', 'Aikido', 'Alpinismo', 'Arrampicata', 'Artistic swimming', 'Atletica', 'Badminton', 'Baseball', 'Softball', 'Beach volley', 'Boogie-woogie', 'Calcio', 'Calcio gaelico', 'Canoismo', 'Canottaggio', 'Capoeira escolar', 'Ciclismo', 'Ciclismo su pista', 'Ciclismo su strada', 'Ciclocross', 'Corsa d’orientamento', 'Curling', 'Danza', 'Danza standard/latine', 'Donut Hockey', 'Flag football', 'FooBaSKILL', 'Frisbee', 'Futnet', 'Futsal', 'Ginnastica', 'Ginnastica agli attrezzi', 'Ginnastica artistica', 'Ginnastica e danza', 'Ginnastica ritmica', 'Giochi di rinvio', 'Giochi nazionali', 'Golf', 'Hockey inline', 'Hockey su ghiaccio', 'Hockey su prato', 'Hornuss', 'Immersione libera', 'Inline-Skating', 'Intercrosse', 'Ju-Jitsu', 'Judo', 'Karate', 'Kin-Ball', 'Light contact boxing', 'Lotta', 'Lotta svizzera', 'Madball', 'Minigolf', 'Mountainbike', 'Netzball', 'Nordic Walking', 'Nuoto', 'Nuoto di salvataggio', 'Pallacanestro', 'Pallacesto', 'Pallamano', 'Pallanuoto', 'Pallapugno', 'Pallavolo', 'Parkour', 'Pattinaggio artistico', 'Pilates', 'Poull Ball', 'Racchette da neve', 'Rafroball', 'Rhönrad', 'Rock’n’roll', 'Roundnet', 'Rugby', 'Running', 'Salto con gli sci', 'Scherma', 'Sci', 'Sci di fondo', 'Sci-escursionismo', 'Skateboard/Waveboard', 'Slackline', 'Smolball', 'Snowboard', 'Sport degli adulti', 'Sport di campo/trekking', 'Sport equestri', 'Sport freestyle', 'Sport in carrozzella', 'Sport scolastico', 'Sprint/Staffetta', 'Squash', 'Stand up paddle', 'Street racket', 'Tchoukball', 'Tennis', 'Tennis da tavolo', 'Tiro sportivo', 'Touchrugby', 'Trail running', 'Trampolino', 'Triathlon', 'Tuffi', 'Unihockey', 'Vela', 'Volteggio', 'Yoga']
sport_events = []

input_folder = 'Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv'

filenames = [os.path.join(input_folder, filename) for filename in sorted(os.listdir('Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv'))]

for filename in filenames:
    
    df = pd.read_csv(filename)
    df = df.map(lambda x: None if pd.isna(x) else x)

    filtered_rows = []

    for index, row in df.iterrows():

        row_str = " ".join(str(field) for field in row if field)
        row_str = row_str.lower()

        for sport in sports:

            if len(re.findall(r'\b' + re.escape(sport.lower()) + r'\b', row_str)):
                sport_events.append([sport, row.tolist()])
                filtered_rows.append(row.tolist())
                break
    
    if not len(filtered_rows):
        os.remove(filename)
        continue

    df = pd.DataFrame(data=filtered_rows, columns=df.columns)
    df.to_csv(filename, index=False, sep=",")