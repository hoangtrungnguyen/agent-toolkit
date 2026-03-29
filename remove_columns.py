import csv
import os

def remove_columns(file_path):
    temp_file = file_path + '.tmp'
    with open(file_path, mode='r', encoding='utf-8') as infile, \
         open(temp_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        try:
            header = next(reader)
        except StopIteration:
            return
            
        # Find indices of columns to remove ('raw_data' and 'expired_date')
        indices_to_remove = set()
        for i, h in enumerate(header):
            clean_h = h.strip()
            if clean_h == 'raw_data' or clean_h == 'expired_date':
                indices_to_remove.add(i)
                
        def filter_row(row):
            return [col for i, col in enumerate(row) if i not in indices_to_remove]
            
        # Write new header
        writer.writerow(filter_row(header))
        
        # Write remaining rows
        for row in reader:
            writer.writerow(filter_row(row))
            
    # Replace original file
    os.replace(temp_file, file_path)
    print(f"Successfully removed raw_data and expired_date columns from {file_path}")

if __name__ == '__main__':
    csv_file = '/Users/trungnguyenhoang/IdeaProjects/agent-utilities/blacklist_luckydraw_campaign_2026.csv'
    remove_columns(csv_file)
