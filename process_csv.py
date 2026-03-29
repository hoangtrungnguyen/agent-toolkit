import csv
import os
from datetime import datetime, timezone, timedelta

def process_csv(file_path):
    # Calculate epoch time for 23:59:59 10-07-2026 GMT+7
    tz = timezone(timedelta(hours=7))
    dt = datetime(2026, 7, 10, 23, 59, 59, tzinfo=tz)
    expired_date_epoch = int(dt.timestamp())

    temp_file = file_path + '.tmp'
    with open(file_path, mode='r', encoding='utf-8') as infile, \
         open(temp_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Original fieldnames
        fieldnames = list(reader.fieldnames)
        
        # Clean up fieldnames: strip spaces
        clean_fieldnames = [f.strip() if f else f for f in fieldnames]
        
        # Rename HO_TEN to full_name and CCCD to document_id
        renamed_fields = []
        for f in fieldnames:
            clean_f = f.strip() if f else f
            if clean_f == 'HO_TEN':
                renamed_fields.append('full_name')
            elif clean_f.upper() == 'CCCD':
                renamed_fields.append('document_id')
            else:
                renamed_fields.append(f)
                
        # Define new columns
        new_columns = ['product_id', 'product_scheme', 'segment_code', 'raw_data', 'expired_date']
        
        # Check if segment_code already exists to decide whether to add or just update
        if 'segment_code' in renamed_fields:
            new_columns.remove('segment_code')
            
        final_fieldnames = renamed_fields + new_columns
        
        writer = csv.DictWriter(outfile, fieldnames=final_fieldnames)
        writer.writeheader()
        
        for row in reader:
            new_row = {}
            for orig_f, new_f in zip(fieldnames, renamed_fields):
                new_row[new_f] = row[orig_f]
            
            # Add new values
            new_row['product_id'] = 'TIME_DEPOSIT'
            new_row['product_scheme'] = 'VIKKI_BANK_STAFF_TD_CAMPAIGN'
            new_row['segment_code'] = 'VIKKI_BANK_STAFF_TD_LUCKYDRAW_2026_SEASON_1'
            new_row['raw_data'] = '' # null value in csv is usually empty string
            new_row['expired_date'] = expired_date_epoch
            
            writer.writerow(new_row)
            
    # Replace original file
    os.replace(temp_file, file_path)
    print(f"Successfully processed {file_path}")

if __name__ == '__main__':
    csv_file = '/Users/trungnguyenhoang/IdeaProjects/agent-utilities/blacklist_luckydraw_campaign_2026.csv'
    process_csv(csv_file)
