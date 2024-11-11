import os
import pandas as pd

directory = "Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/fixed_csv"

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        if df.empty:
            os.remove(file_path)
            print(f"Deleted empty file: {filename}")