import os
import pandas as pd
import argparse
import sys
import csv
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_chunk(chunk, search_term, search_column):
    """Worker function to process a single DataFrame chunk."""
    search_term_lower = search_term.lower()
    
    if search_column:
        if search_column not in chunk.columns:
            return None # Skip
        search_chunk = chunk[[search_column]]
    else:
        search_chunk = chunk

    mask = search_chunk.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False))
    
    matches = []
    for row_idx in range(len(chunk)):
        if mask.iloc[row_idx].any():
            match_row = chunk.iloc[row_idx]
            matched_in_cols = [search_chunk.columns[c] for c in range(len(search_chunk.columns)) if mask.iloc[row_idx, c]]
            matches.append((row_idx, match_row, matched_in_cols))
            
    return matches

def search_text(search_term, path=None, directory='.', output_file=None, search_column=None, display_columns=None, pretty=False, chunk_size=1000, workers=1, resume=False, encoding='utf-8', delimiter=',', compression='infer'):
    search_term_lower = search_term.lower()
    found_count = 0
    display_cols_list = [c.strip() for c in display_columns.split(',')] if display_columns else None
    
    # Decide what to search: specific file or directory
    if path and os.path.isfile(path):
        targets = [path]
    elif directory and os.path.isdir(directory):
        targets = sorted([os.path.join(directory, f) for f in os.listdir(directory) 
                   if f != output_file and not f.startswith('.')])
    else:
        print(f"Error: Invalid path or directory specified.")
        return 0

    out_f = None
    csv_writer = None
    output_headers_init = False
    is_csv_output = False

    if output_file:
        ext = os.path.splitext(output_file)[1].lower()
        is_csv_output = (ext == '.csv')
        try:
            # Append if resuming, otherwise overwrite
            mode = 'a' if resume and os.path.exists(output_file) else 'w'
            out_f = open(output_file, mode=mode, encoding='utf-8', newline='')
            if mode == 'a' and os.path.getsize(output_file) > 0:
                output_headers_init = True
                
            if is_csv_output:
                csv_writer = csv.writer(out_f)
            elif mode == 'w':
                out_f.write(f"# Search Results for '{search_term}'\n\n")
                out_f.write("| File | Line | Match Columns | Content |\n")
                out_f.write("| --- | --- | --- | --- |\n")
        except Exception as e:
            print(f"Error opening output file: {e}")
            return 0

    checkpoint_file = ".search_checkpoint.json"
    checkpoints = {}
    if resume and os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                checkpoints = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load checkpoint file: {e}")

    try:
        for file_path in targets:
            filename = os.path.basename(file_path)
            
            if filename.endswith('.csv'):
                try:
                    start_chunk_index = checkpoints.get(file_path, 0)
                    row_offset = 2 + (start_chunk_index * chunk_size)
                    
                    csv_reader = pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding, sep=delimiter, compression=compression)
                    
                    # skip to start_chunk_index
                    for _ in range(start_chunk_index):
                        try:
                            next(csv_reader)
                        except StopIteration:
                            break
                    
                    # Parallel processing for chunks
                    if workers > 1:
                        with ProcessPoolExecutor(max_workers=workers) as executor:
                            futures = []
                            chunk_offsets = []
                            for chunk_idx, chunk in enumerate(csv_reader, start=start_chunk_index):
                                futures.append((chunk_idx, executor.submit(process_chunk, chunk, search_term, search_column)))
                                chunk_offsets.append(row_offset)
                                row_offset += len(chunk)
                                
                                # initialize headers on first chunk
                                if is_csv_output and not output_headers_init:
                                    meta_headers = ['_source_file', '_source_line', '_match_columns']
                                    cols_to_save = display_cols_list if display_cols_list else list(chunk.columns)
                                    csv_writer.writerow(meta_headers + cols_to_save)
                                    output_headers_init = True
                                    
                            for (chunk_idx, future), offset in zip(futures, chunk_offsets):
                                matches = future.result()
                                if matches is not None:
                                    for row_idx, match_row, matched_in_cols in matches:
                                        # Prepare display data
                                        if display_cols_list:
                                            display_data = {c: match_row[c] if c in match_row else "N/A" for c in display_cols_list}
                                        else:
                                            display_data = match_row.to_dict()

                                        # Console Output
                                        print(f"\n--- [{filename}] Match found on Line {row_idx + offset} ---")
                                        if pretty:
                                            for col, val in display_data.items():
                                                indicator = " ⭐" if col in matched_in_cols else ""
                                                print(f"  {col:20}: {val}{indicator}")
                                        else:
                                            display_str = ", ".join([f"{k}: {v}" for k, v in display_data.items()])
                                            print(f"  👉 {display_str}")
                                        
                                        if out_f:
                                            save_row = [filename, row_idx + offset, ", ".join(matched_in_cols)]
                                            if is_csv_output:
                                                save_row += [display_data.get(c, "") for c in (display_cols_list if display_cols_list else match_row.index)]
                                                csv_writer.writerow(save_row)
                                            else:
                                                content_summary = ", ".join([f"{k}: {v}" for k, v in display_data.items()])
                                                out_f.write(f"| {filename} | {row_idx + offset} | {', '.join(matched_in_cols)} | {content_summary} |\n")
                                        
                                        found_count += 1
                                
                                checkpoints[file_path] = chunk_idx + 1
                                if resume:
                                    with open(checkpoint_file, 'w') as f:
                                        json.dump(checkpoints, f)
                                    
                    else:
                        # Sequential chunk processing
                        for chunk_idx, chunk in enumerate(csv_reader, start=start_chunk_index):
                            matches = process_chunk(chunk, search_term, search_column)
                            
                            if is_csv_output and not output_headers_init:
                                meta_headers = ['_source_file', '_source_line', '_match_columns']
                                cols_to_save = display_cols_list if display_cols_list else list(chunk.columns)
                                csv_writer.writerow(meta_headers + cols_to_save)
                                output_headers_init = True
                                
                            if matches:
                                for row_idx, match_row, matched_in_cols in matches:
                                    if display_cols_list:
                                        display_data = {c: match_row[c] if c in match_row else "N/A" for c in display_cols_list}
                                    else:
                                        display_data = match_row.to_dict()

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
                                            save_row += [display_data.get(c, "") for c in (display_cols_list if display_cols_list else match_row.index)]
                                            csv_writer.writerow(save_row)
                                        else:
                                            content_summary = ", ".join([f"{k}: {v}" for k, v in display_data.items()])
                                            out_f.write(f"| {filename} | {row_idx + row_offset} | {', '.join(matched_in_cols)} | {content_summary} |\n")
                                    
                                    found_count += 1
                            
                            row_offset += len(chunk)
                            checkpoints[file_path] = chunk_idx + 1
                            if resume:
                                with open(checkpoint_file, 'w') as f:
                                    json.dump(checkpoints, f)
                                    
                except Exception as e:
                    print(f"Error reading {filename} with pandas: {e}")
            
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
        parser = argparse.ArgumentParser(description='Search for text in files with streaming and parallel processing.')
        parser.add_argument('term', help='The text to search for.')
        parser.add_argument('--path', help='Specific file path to search.')
        parser.add_argument('--dir', default='.', help='Directory to search (default: current directory).')
        parser.add_argument('--output', help='Output file to save results (.csv or .md).')
        parser.add_argument('--search-column', help='Only search within this specific column.')
        parser.add_argument('--display-columns', help='Comma-separated list of columns to show in output.')
        parser.add_argument('--pretty', action='store_true', help='Use a vertical, readable format for console output.')
        parser.add_argument('--chunk-size', type=int, default=1000, help='Number of rows to process per chunk.')
        parser.add_argument('--workers', type=int, default=1, help='Number of CPU cores to use for parallel processing.')
        parser.add_argument('--resume', action='store_true', help='Resume processing from the last checkpoint.')
        parser.add_argument('--encoding', default='utf-8', help='File encoding (default: utf-8).')
        parser.add_argument('--delimiter', default=',', help='CSV delimiter (default: comma).')
        parser.add_argument('--compression', default='infer', help='Compression format (e.g., gzip, bz2, zip, infer).')

        args = parser.parse_args()

        total_found = search_text(
            args.term, 
            path=args.path, 
            directory=args.dir, 
            output_file=args.output,
            search_column=args.search_column,
            display_columns=args.display_columns,
            pretty=args.pretty,
            chunk_size=args.chunk_size,
            workers=args.workers,
            resume=args.resume,
            encoding=args.encoding,
            delimiter=args.delimiter,
            compression=args.compression
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