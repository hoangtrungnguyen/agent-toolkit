from csv_reader import CSVProcessor
import sys

def list_promocodes(file_path):
    processor = CSVProcessor(file_path)
    
    # 1. Get header to identify the correct column
    header = processor.get_header()
    print(f"File Columns: {header}")
    
    # Try to find a column that looks like a promocode
    promo_col = None
    candidates = ['promocode', 'promo_code', 'promo', 'coupon', 'code', 'discount_code']
    
    for col in header:
        if col.lower().strip() in candidates:
            promo_col = col
            break
            
    if not promo_col:
        # If no exact match, try partial match
        for col in header:
            if any(cand in col.lower() for cand in candidates):
                promo_col = col
                break
    
    if not promo_col:
        print("Error: Could not automatically identify a 'promocode' column.")
        return

    print(f"Identified promocode column: '{promo_col}'")
    
    # 2. Extract unique codes using the stream_rows method for performance
    unique_codes = set()
    for row in processor.stream_rows():
        code = row.get(promo_col)
        if code and code.strip():
            unique_codes.add(code.strip())
            
    print(f"\nFound {len(unique_codes)} unique promocodes:\n")
    for code in sorted(list(unique_codes)):
        print(f"- {code}")

if __name__ == "__main__":
    target_file = "/home/htnguyen/Downloads/New_Query_2026_02_24 (1).csv"
    list_promocodes(target_file)
