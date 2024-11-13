import os
import pandas as pd

# Directory containing the CSV files
csv_dir = '/home/pietro/Desktop/UniTn/5_anno/Knowledge Graph Engineering (??)/knowledge-graph-engineering-project/Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv'

# List to hold dataframes
dfs = []

# Iterate over all files in the directory
for filename in sorted(os.listdir(csv_dir)):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(file_path)
        df['municipality'] = filename
        dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged dataframe to a new CSV file
output_path = os.path.join(csv_dir, 'merged_data.csv')
merged_df.to_csv(output_path, index=False)

print(f'Merged data saved to {output_path}')