import csv
from csv_reader import CSVProcessor

def check_max_usage(file_path):
    processor = CSVProcessor(file_path)
    processor.dialect = csv.excel # Force comma delimiter
    count = 1
    found = False
    
    print(f"Checking for maxusage > 200 in {file_path}...")
    
    for row in processor.stream_rows():
        try:
            max_usage = int(row['maxusage'])
            if max_usage > 200:
                print(f"Found: Row {count} has maxusage {max_usage} (ID: {row['id']})")
                found = True
        except (ValueError, KeyError) as e:
            # Handle potential non-integer values or missing columns
            pass
        count += 1
    
    if not found:
        print("No rows found with maxusage larger than 200.")
    else:
        print("Finished checking.")

if __name__ == "__main__":
    csv_path = "/home/htnguyen/Downloads/612355_2026_02_25.csv"
    check_max_usage(csv_path)
