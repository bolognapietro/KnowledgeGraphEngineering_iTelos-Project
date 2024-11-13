import pandas as pd
import os

# Define file paths
file_path = os.path.join('Phase 2 - Information Gathering', 'data', 'standardized', 'events', 'Event.csv')
output_path = file_path

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load the CSV file
df = pd.read_csv(file_path)

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert date columns to datetime format
# Using a custom date parser to handle various formats
df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce', format='mixed')
df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce', format='mixed')

# Format datetime columns to consistent string format
# For startDate, convert NaT to empty string
df['startDate'] = df['startDate'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else '')

# For endDate, convert NaT to empty string
df['endDate'] = df['endDate'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else '')

# Save the standardized file
df.to_csv(output_path, index=False)

print(f"File processed successfully. Output saved to: {output_path}")