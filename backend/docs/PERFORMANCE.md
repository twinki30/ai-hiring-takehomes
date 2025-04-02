# PERFORMANCE.md

## Overview
This document outlines the performance optimization strategies and benchmarks used in the serverless pipeline designed to process high-volume geospatial telemetry data for delivery vehicles. The primary goal is to minimize memory usage, enhance throughput, and ensure low-latency processing while meeting the constraints of AWS Lambda's 512MB memory limit.

## 1. Memory Management Strategies

### a. Using Generators and Iterators
Generators are employed to process telemetry data in chunks, thus avoiding the need to load entire CSV files into memory at once. This allows for memory-efficient processing even when dealing with large datasets.

```python
import csv
from pathlib import Path
from typing import Generator

# Generator to yield rows in chunks
def stream_csv_in_chunks(file_path: Path) -> Generator[list, None, None]:
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        buffer = []
        for row in reader:
            buffer.append(row)
            if len(buffer) >= 10_000:  # Yield after every 10,000 rows
                yield buffer
                buffer = []
        if buffer:
            yield buffer
