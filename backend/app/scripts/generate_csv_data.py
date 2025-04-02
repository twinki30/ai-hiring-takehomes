import csv
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()

OUTPUT_DIR = Path("data/telemetry")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VEHICLE_COUNT = 5000  # Pool of unique vehicles
FILES_TO_GENERATE = 10
ROWS_PER_FILE = 100_000

ENGINE_STATUSES = ["moving", "idle"]

# Pre-generate vehicle IDs
vehicle_ids = [f"VH_{str(i).zfill(5)}" for i in range(1, VEHICLE_COUNT + 1)]

def generate_row():
    vehicle_id = random.choice(vehicle_ids)
    timestamp = datetime.utcnow().isoformat()
    lat = round(random.uniform(-90.0, 90.0), 6)
    lon = round(random.uniform(-180.0, 180.0), 6)
    speed_kmh = random.randint(0, 120)
    engine_status = random.choice(ENGINE_STATUSES)
    fuel_level = random.randint(0, 100)
    return [vehicle_id, timestamp, lat, lon, speed_kmh, engine_status, fuel_level]

def generate_csv_file(index):
    file_path = OUTPUT_DIR / f"telemetry_{index}.csv"
    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["vehicle_id", "timestamp", "lat", "lon", "speed_kmh", "engine_status", "fuel_level"])
        for _ in range(ROWS_PER_FILE):
            writer.writerow(generate_row())
    print(f"Generated: {file_path}")

if __name__ == "__main__":
    for i in range(1, FILES_TO_GENERATE + 1):
        generate_csv_file(i)
