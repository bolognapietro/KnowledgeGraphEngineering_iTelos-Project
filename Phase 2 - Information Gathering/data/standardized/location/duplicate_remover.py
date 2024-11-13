import pandas as pd

# Load the CSV file
input_file = 'Phase 2 - Information Gathering/data/standardized/location/Location.csv'
output_file = 'Phase 2 - Information Gathering/data/standardized/location/Location_deduplicated.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Drop duplicate rows based on the 'address' column
df_deduplicated = df.drop_duplicates(subset='address')

# Write the deduplicated DataFrame to a new CSV file
df_deduplicated.to_csv(output_file, index=False)

print(f"Deduplicated file saved to {output_file}")