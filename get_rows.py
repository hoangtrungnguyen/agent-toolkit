import csv
import json
from csv_reader import CSVProcessor

def get_rows_by_ids(file_path, target_ids):
    processor = CSVProcessor(file_path)
    processor.dialect = csv.excel # Ensure comma delimiter
    
    results = []
    print(f"Searching for IDs {target_ids} in {file_path}...")
    
    for row in processor.stream_rows():
        if row['id'] in target_ids:
            results.append(row)
            if len(results) == len(target_ids):
                break
                
    for res in results:
        print(f"\n--- ID: {res['id']} ---")
        # Pretty print the row dictionary
        for key, value in res.items():
            if key == 'additional_data':
                # Try to pretty print the JSON string inside additional_data
                try:
                    # The data looks like it uses single quotes, which isn't valid JSON, 
                    # but let's see if we can safely format it or just print it.
                    # It seems to be a Python string representation of a dict.
                    print(f"{key}: {value}")
                except:
                    print(f"{key}: {value}")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    csv_path = "/home/htnguyen/Downloads/612355_2026_02_25.csv"
    get_rows_by_ids(csv_path, ['491', '492'])
