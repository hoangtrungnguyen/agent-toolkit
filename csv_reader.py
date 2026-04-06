import csv
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Generator

# Set up professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CSVProcessor")

class CSVProcessor:
    """
    A pro-ready CSV processor designed for AI agents.
    Provides robust reading, error handling, and data inspection capabilities
    using only the Python standard library.
    """

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {self.file_path}")
        
        self.encoding = 'utf-8' # Default
        self.dialect: Optional[csv.Dialect] = None
        self._header: Optional[List[str]] = None

    def _detect_dialect(self, sample_size: int = 4096) -> csv.Dialect:
        """
        Sniffs the CSV to detect delimiter, quote character, etc.
        """
        try:
            with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
                sample = f.read(sample_size)
                sniffer = csv.Sniffer()
                # Check if it has a header
                has_header = sniffer.has_header(sample)
                dialect = sniffer.sniff(sample)
                logger.info(f"Detected dialect: delimiter='{dialect.delimiter}', quotechar='{dialect.quotechar}'")
                return dialect
        except Exception as e:
            logger.warning(f"Could not automatically detect dialect: {e}. Falling back to defaults.")
            return csv.excel # Default Excel-style CSV

    def get_header(self) -> List[str]:
        """
        Returns the column names of the CSV.
        """
        if self._header:
            return self._header
        
        dialect = self.dialect or self._detect_dialect()
        with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
            reader = csv.reader(f, dialect=dialect)
            self._header = next(reader)
        return self._header

    def read_rows(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Reads CSV rows into a list of dictionaries.
        
        Args:
            limit: Maximum number of rows to return.
            offset: Number of rows to skip (after header).
            
        Returns:
            A list of rows, where each row is a dictionary (column_name: value).
        """
        dialect = self.dialect or self._detect_dialect()
        data = []
        try:
            with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
                reader = csv.DictReader(f, dialect=dialect)
                
                # Skip offset
                for _ in range(offset):
                    try:
                        next(reader)
                    except StopIteration:
                        break
                
                # Read rows up to limit
                count = 0
                for row in reader:
                    if limit is not None and count >= limit:
                        break
                    data.append(dict(row))
                    count += 1
            
            logger.info(f"Read {len(data)} rows from {self.file_path}")
            return data
        except csv.Error as e:
            logger.error(f"CSV error while reading {self.file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error reading {self.file_path}: {e}")
            raise

    def stream_rows(self) -> Generator[Dict[str, Any], None, None]:
        """
        A memory-efficient generator for streaming large CSV files.
        """
        dialect = self.dialect or self._detect_dialect()
        with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
            reader = csv.DictReader(f, dialect=dialect)
            for row in reader:
                yield dict(row)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Gathers metadata about the CSV file useful for AI agents to understand the context.
        """
        header = self.get_header()
        file_stats = self.file_path.stat()
        
        # Approximate row count (careful with large files)
        # For a truly pro-ready agent, we might want a fast count vs accurate count
        row_count = 0
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            row_count = sum(1 for _ in f) - 1 # Subtract header
            
        return {
            "filename": self.file_path.name,
            "absolute_path": str(self.file_path.absolute()),
            "file_size_bytes": file_stats.st_size,
            "columns": header,
            "column_count": len(header),
            "approx_row_count": row_count
        }

if __name__ == "__main__":
    # Example usage for demonstration
    # 1. Create a dummy CSV for testing
    test_file = "sample_data.csv"
    with open(test_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "role", "salary"])
        writer.writerow([1, "Alice", "Engineer", 120000])
        writer.writerow([2, "Bob", "Designer", 95000])
        writer.writerow([3, "Charlie", "Product Manager", 110000])

    print("--- CSV Processor Demo ---")
    try:
        processor = CSVProcessor(test_file)
        
        print("\n1. Metadata:")
        metadata = processor.get_metadata()
        for k, v in metadata.items():
            print(f"  {k}: {v}")
            
        print("\n2. First 2 rows:")
        rows = processor.read_rows(limit=2)
        for row in rows:
            print(f"  {row}")
            
        print("\n3. Streaming all names:")
        for row in processor.stream_rows():
            print(f"  Name: {row['name']}")
            
    finally:
        # Cleanup test file
        if os.path.exists(test_file):
            os.remove(test_file)
