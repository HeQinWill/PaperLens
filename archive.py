from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Get the current year and month
current_date = datetime.now().strftime("%Y%m%d")

# Path to the paper_entries directory
paper_entries_dir = Path('./paper_entries')

# If there is not relevant papers in the last period
# we will not delete the original files first
not_relevant_files = list(paper_entries_dir.glob('*_not_relevant.csv'))
if len(not_relevant_files) == 0:
    print("No not relevant papers in the last period")
else:
    for f in not_relevant_files:
        # Get the file date from the file name
        file_date = f.name.split('_')[-3]

        # Convert file_date to datetime
        file_date = datetime.strptime(file_date, "%Y%m%d")

        # Delete it when file_date is older than current_date - 14 days
        if file_date < datetime.now() - timedelta(days=14):
            f.unlink()
            print(f"Deleted: {f}")

# Get all CSV files in this period
csv_files = sorted(paper_entries_dir.glob('20*.csv'))
print('Number of CSV files:', len(csv_files))

# List to store dataframes
dfs = []

# Read each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# # Show the duplicates
# print(merged_df[merged_df.duplicated(subset=['doi', 'title'])].sort_values('title'))

# Remove duplicates based on 'doi'
merged_df.drop_duplicates(subset=['doi', 'title'], keep='last', inplace=True)

# Get the relevant papers or not
relevant_true = merged_df[merged_df['is_relevant'] == True]
relevant_false = merged_df[merged_df['is_relevant'] == False]

# Save the merged CSV
output_file = paper_entries_dir / f"archive_{current_date}.csv"
relevant_true.to_csv(output_file, index=False)
print(f"Merged CSV saved to {output_file}")

output_file = paper_entries_dir / f"archive_{current_date}_not_relevant.csv"
relevant_false.to_csv(output_file, index=False)
print(f"Not relevant CSV saved to {output_file}")

# Delete original files
for file in csv_files:
    file.unlink()
    print(f"Deleted: {file}")