import pandas as pd
import argparse
import os

def get_csv_headers(file_path):
    """
    Retrieves the headers of a CSV file without reading the actual data content.
    """
    try:
        # Use nrows=0 to read only the header row
        df = pd.read_csv(file_path, nrows=0)
        return list(df.columns)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get headers of a CSV file efficiently.')
    parser.add_argument('path', help='Path to the CSV file.')

    args = parser.parse_args()

    if os.path.isfile(args.path):
        headers = get_csv_headers(args.path)
        if isinstance(headers, list):
            print(f"Headers for '{os.path.basename(args.path)}':")
            for i, header in enumerate(headers, start=1):
                print(f"  {i}. {header}")
        else:
            print(headers)
    else:
        print(f"Error: File '{args.path}' not found.")
