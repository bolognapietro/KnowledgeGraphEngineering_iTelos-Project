import csv
import os
import pandas as pd

# Define the input and output directories
input_dir = 'Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/csv'
output_dir = 'Phase 2 - Information Gathering/data/cleaned/dati.trentino.it/fixed_csv'
log_file = 'log.txt'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open the log file in write mode
with open(log_file, 'w') as log:
    # Process each CSV file in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)

            # Replace semicolons with commas in the input file
            with open(input_file, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(';', ',')

            with open(input_file, 'w') as file:
                file.write(filedata)

            # Define a custom function to handle bad lines and log warnings
            def log_bad_line(bad_line):
                log.write(f"Warning in file {filename}: {bad_line}\n")

            # Load the CSV file with error handling, quoting, and using the Python engine
            try:
                # Attempt to load and log problematic lines
                df = pd.read_csv(
                    input_file,
                    delimiter=',',          # Specify delimiter as comma
                    quoting=csv.QUOTE_ALL,  # Handle quoted fields properly
                    engine='python',        # Use the Python engine for better flexibility
                    on_bad_lines=log_bad_line  # Use custom function to log bad lines
                )

                # Get expected number of columns from the header
                expected_columns = len(df.columns)

                # Filter out rows with incorrect column count
                df_clean = df[df.apply(lambda x: len(x) == expected_columns, axis=1)]

                # Save the cleaned DataFrame to a new CSV file
                df_clean.to_csv(output_file, index=False)

                print(f"Cleaning successful! Cleaned file saved as: {output_file}")

            except Exception as e:
                log.write(f"Error occurred while processing {filename}: {e}\n")
                print(f"Error occurred while processing {filename}: {e}")

print(f"Processing complete. Check {log_file} for details on warnings.")
