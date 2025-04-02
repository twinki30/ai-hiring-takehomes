import csv
from pathlib import Path
from typing import Generator
from app.services.redis_cache import load_metadata_to_cache, is_valid_speed

TELEMETRY_DIR = Path("data/telemetry")
CHUNK_SIZE = 10_000

# Generator to yield rows in chunks
def stream_csv_in_chunks(file_path: Path) -> Generator[list, None, None]:
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        buffer = []
        for row in reader:
            buffer.append(row)
            if len(buffer) >= CHUNK_SIZE:
                yield buffer
                buffer = []
        if buffer:
            yield buffer

# Validate a single record
def validate_row(row: dict) -> bool:
    try:
        lat = float(row["lat"])
        speed = float(row["speed_kmh"])
        if lat > 90:
            return False
        return is_valid_speed(row["vehicle_id"], speed)
    except Exception:
        return False

# Process all CSV files
def process_all_csv():
    for file_path in TELEMETRY_DIR.glob("*.csv"):
        print(f"Processing: {file_path.name}")
        for chunk in stream_csv_in_chunks(file_path):
            valid_rows = [row for row in chunk if validate_row(row)]
            print(f"  Valid: {len(valid_rows)} / {len(chunk)}")

if __name__ == "__main__":
    load_metadata_to_cache()
    process_all_csv()
