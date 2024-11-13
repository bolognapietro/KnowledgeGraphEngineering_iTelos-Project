import pandas as pd

# Percorsi del file
input_file = 'Phase 2 - Information Gathering/data/standardized/sport/SportFacility.csv'
output_file = 'Phase 2 - Information Gathering/data/standardized/sport/mod_SportFacility.csv'

# Carica il file CSV
df = pd.read_csv(input_file)

# Funzione di trasformazione della colonna 'sports'
def transform_sports(sports_value):
    # Rimuove le parentesi quadre
    sports_value = sports_value.strip("[]")
    
    # Converte in lista di numeri (separati da virgola)
    sports_list = [int(x) for x in sports_value.split(",") if x.strip().isdigit()]
    
    # Applica le modifiche richieste
    updated_sports_list = [
        6 if x == 122 else (x - 1 if x >= 123 else x) for x in sports_list
    ]
    
    # Ritorna la lista come stringa
    return ",".join(map(str, updated_sports_list))

# Applica la funzione alla colonna 'sports'
df['sports'] = df['sports'].apply(transform_sports)

# Salva il risultato in un nuovo file CSV
df.to_csv(output_file, index=False)

print(f"Modifiche completate! File salvato come {output_file}")
