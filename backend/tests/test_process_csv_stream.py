import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import tempfile
import csv
import os

from app.scripts.process_csv_stream import stream_csv_in_chunks, validate_row

class TestProcessCSVStream(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
        self.writer = csv.writer(self.temp_file)
        self.writer.writerow(["vehicle_id", "timestamp", "lat", "lon", "speed_kmh", "engine_status", "fuel_level"])
        self.writer.writerow(["VH_00001", "2023-10-10T12:00:00", "40.7128", "-74.0060", "45", "moving", "75"])
        self.writer.writerow(["VH_00002", "2023-10-10T12:00:01", "91.0000", "-74.0060", "45", "idle", "60"])  # invalid lat
        self.temp_file.close()
        self.file_path = Path(self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_stream_csv_in_chunks(self):
        chunks = list(stream_csv_in_chunks(self.file_path))
        self.assertEqual(len(chunks), 1)
        self.assertEqual(len(chunks[0]), 2)
        self.assertEqual(chunks[0][0]["vehicle_id"], "VH_00001")

    @patch('app.scripts.process_csv_stream.is_valid_speed')
    def test_validate_row_valid(self, mock_valid_speed):
        mock_valid_speed.return_value = True
        row = {
            "vehicle_id": "VH_00001",
            "lat": "40.7128",
            "speed_kmh": "45"
        }
        self.assertTrue(validate_row(row))

    @patch('app.scripts.process_csv_stream.is_valid_speed')
    def test_validate_row_invalid_lat(self, mock_valid_speed):
        mock_valid_speed.return_value = True
        row = {
            "vehicle_id": "VH_00001",
            "lat": "91.0000",  # Invalid latitude
            "speed_kmh": "45"
        }
        self.assertFalse(validate_row(row))

    def test_validate_row_malformed_data(self):
        row = {
            "vehicle_id": "VH_00001",
            "lat": "not-a-float",
            "speed_kmh": "fast"
        }
        self.assertFalse(validate_row(row))


if __name__ == '__main__':
    unittest.main()
