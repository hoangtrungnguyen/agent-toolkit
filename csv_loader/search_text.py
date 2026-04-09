import os
import pandas as pd
import argparse
import sys
import csv

def search_text(search_term, path=None, directory='.', output_file=None, search_column=None, display_columns=None, pretty=False):
    search_term_lower = search_term.lower()
    found_count = 0
    display_cols_list = [c.strip() for c in display_columns.split(',')] if display_columns else None
    
    # Decide what to search: specific file or directory
    if path and os.path.isfile(path):
        targets = [path]
    elif directory and os.path.isdir(directory):
        # Exclude our own results and binary/ignored files
        targets = sorted([os.path.join(directory, f) for f in os.listdir(directory) 
                   if f != output_file and not f.startswith('.')])
    else:
        print(f"Error: Invalid path or directory specified.")
        return 0

    # Open output file if specified
    out_f = None
    csv_writer = None
    output_headers_init = False
    is_csv_output = False

    if output_file:
        ext = os.path.splitext(output_file)[1].lower()
        is_csv_output = (ext == '.csv')
        try:
            out_f = open(output_file, mode='w', encoding='utf-8', newline='')
            if is_csv_output:
                csv_writer = csv.writer(out_f)
            else:
                out_f.write(f"# Search Results for '{search_term}'\n\n")
                out_f.write("| File | Line | Match Columns | Content |\n")
                out_f.write("| --- | --- | --- | --- |\n")
        except Exception as e:
            print(f"Error opening output file: {e}")
            return 0

    try:
        for file_path in targets:
            filename = os.path.basename(file_path)
            
            # Using pandas for CSV files with chunking
            if filename.endswith('.csv'):
                try:
                    row_offset = 2
                    for chunk in pd.read_csv(file_path, chunksize=1000):
                        # Determine columns to search
                        if search_column:
                            if search_column not in chunk.columns:
                                print(f"Warning: Column '{search_column}' not found in {filename}. Skipping search in this file.")
                                break
                            search_chunk = chunk[[search_column]]
                        else:
                            search_chunk = chunk

                        mask = search_chunk.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False))
                        
                        # Initialize CSV output header
                        if is_csv_output and not output_headers_init:
                            meta_headers = ['_source_file', '_source_line', '_match_columns']
                            # If display_columns is set, only output those in the CSV as well
                            cols_to_save = display_cols_list if display_cols_list else list(chunk.columns)
                            csv_writer.writerow(meta_headers + cols_to_save)
                            output_headers_init = True

                        for row_idx in range(len(chunk)):
                            if mask.iloc[row_idx].any():
                                match_row = chunk.iloc[row_idx]
                                # Identify which columns actually matched (within our search set)
                                matched_in_cols = [search_chunk.columns[c] for c in range(len(search_chunk.columns)) if mask.iloc[row_idx, c]]
                                
                                # Prepare display data
                                if display_cols_list:
                                    display_data = {c: match_row[c] if c in match_row else "N/A" for c in display_cols_list}
                                else:
                                    display_data = match_row.to_dict()

                                # Console Output
                                print(f"\n--- [{filename}] Match found on Line {row_idx + row_offset} ---")
                                if pretty:
                                    for col, val in display_data.items():
                                        indicator = " ⭐" if col in matched_in_cols else ""
                                        print(f"  {col:20}: {val}{indicator}")
                                else:
                                    display_str = ", ".join([f"{k}: {v}" for k, v in display_data.items()])
                                    print(f"  👉 {display_str}")
                                
                                if out_f:
                                    save_row = [filename, row_idx + row_offset, ", ".join(matched_in_cols)]
                                    if is_csv_output:
                                        save_row += [display_data.get(c, "") for c in (display_cols_list if display_cols_list else chunk.columns)]
                                        csv_writer.writerow(save_row)
                                    else:
                                        content_summary = ", ".join([f"{k}: {v}" for k, v in display_data.items()])
                                        out_f.write(f"| {filename} | {row_idx + row_offset} | {', '.join(matched_in_cols)} | {content_summary} |\n")
                                
                                found_count += 1
                        row_offset += len(chunk)
                except Exception as e:
                    print(f"Error reading {filename} with pandas: {e}")
            
            # Streaming standard text-based files
            elif filename.endswith(('.txt', '.md', '.log')):
                 try:
                    with open(file_path, mode='r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f, start=1):
                            if search_term_lower in line.lower():
                                stripped_line = line.strip()
                                
                                if is_csv_output and not output_headers_init:
                                    csv_writer.writerow(['_source_file', '_source_line', '_match_columns', 'content'])
                                    output_headers_init = True

                                print(f"\n--- [{filename}] Line {line_idx} ---")
                                print(f"  👉 {stripped_line}")
                                
                                if out_f:
                                    if is_csv_output:
                                        csv_writer.writerow([filename, line_idx, 'N/A', stripped_line])
                                    else:
                                        out_f.write(f"| {filename} | {line_idx} | N/A | {stripped_line} |\n")
                                found_count += 1
                 except Exception as e:
                    print(f"Error reading {filename}: {e}")
    except KeyboardInterrupt:
        print("\nSearch interrupted by user. Finalizing output...")
    finally:
        if out_f:
            out_f.close()
    
    return found_count

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Search for text in files with streaming output.')
        parser.add_argument('term', help='The text to search for.')
        parser.add_argument('--path', help='Specific file path to search.')
        parser.add_argument('--dir', default='.', help='Directory to search (default: current directory).')
        parser.add_argument('--output', help='Output file to save results (.csv or .md).')
        parser.add_argument('--search-column', help='Only search within this specific column.')
        parser.add_argument('--display-columns', help='Comma-separated list of columns to show in output.')
        parser.add_argument('--pretty', action='store_true', help='Use a vertical, readable format for console output.')

        args = parser.parse_args()

        total_found = search_text(
            args.term, 
            path=args.path, 
            directory=args.dir, 
            output_file=args.output,
            search_column=args.search_column,
            display_columns=args.display_columns,
            pretty=args.pretty
        )

        if total_found > 0:
            if args.output:
                print(f"\nSuccessfully found and saved {total_found} matches to '{args.output}'.")
            else:
                print(f"\nTotal matches found: {total_found}")
        else:
            print(f"No matches found for '{args.term}'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
