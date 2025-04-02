# ARCHITECTURE.md

## Overview
This document outlines the high-level architecture for a memory-efficient, serverless pipeline that ingests and processes high-volume GPS telemetry data from over 50,000 delivery vehicles. The architecture is built using AWS serverless components with scalability, low-latency, and cost-optimization as primary goals.

## Architecture Diagram

                         +--------------------------+
                         |   [Vehicle Telemetry]    |
                         |     CSV Generator        |
                         +-----------+--------------+
                                     |
                                     v
                         +--------------------------+
                         |         Amazon S3         |
                         | (Stores Raw CSV Files)    |
                         +-----------+--------------+
                                     |
                                     v  (S3 Event Trigger)
                         +--------------------------+
                         |     AWS Lambda           |
                         | process_csv_stream.py    |
                         | - Streams & validates    |
                         | - Loads metadata to Redis|
                         +-----------+--------------+
                                     |
         +---------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
+------------------+     +-----------------------+     +------------------------+
|  Redis (ElastiCache)|  | SQS (moving priority) |     | SQS (idle priority)    |
| - metadata cache   |  | - Engine status = moving |   | - Engine status = idle |
+------------------+     +-----------------------+     +------------------------+
                                    \                           /
                                     \                         /
                                      \                       /
                                       v                     v
                                  +-------------------------------+
                                  |       AWS Lambda              |
                                  | lambda_handler.py             |
                                  | - Validates speed             |
                                  | - Distance calc               |
                                  | - Deduplicates (Bloom filter) |
                                  | - Writes to DynamoDB          |
                                  | - Publishes to SQS if needed  |
                                  +---------------+---------------+
                                                  |
                                                  v
                                 +-------------------------------+
                                 |       DynamoDB                |
                                 | - TelemetryData Table         |
                                 +-------------------------------+

Optional / Advanced Components:
--------------------------------
                                 +-------------------------------+
                                 |  Dead Letter Queue (DLQ)      |
                                 |  - Failed SQS messages        |
                                 +-------------------------------+
                                                 |
                                                 v
                                  +----------------------------+
                                  | Lambda: dlq_handler.py     |
                                  | - Reprocess or log error   |
                                  +----------------------------+

                                 +-------------------------------+
                                 | CloudWatch Logs & Metrics     |
                                 | - Logs, alerts, autoscaling   |
                                 +-------------------------------+

                                 +-------------------------------+
                                 | S3 Tiered Storage             |
                                 | - Raw CSV → Glacier (7 days)  |
                                 | - Archived in Parquet         |
                                 +-------------------------------+

## Components and Rationale

### 1. **Amazon S3** – *Raw Data Storage*

- Used to store raw CSV files uploaded by the data producer.
- Triggers downstream processing via S3 Event Notifications.
- Supports tiered storage (S3 Standard → Glacier) for cost optimization.

### 2. **AWS Lambda** – *Stateless Processing Logic*

- Handles CSV file processing in a memory-safe, streaming manner.
- Uses generators and chunking (≤100MB) to stay within 512MB memory constraints.
- Filters and validates telemetry records (e.g., lat > 90, speed > max_speed).
- Publishes valid events to respective SQS queues.

### 3. **Amazon ElastiCache (Redis)** – *Caching Layer*

- Caches `metadata_api.json` (e.g., max_speed, depot coordinates) to reduce redundant I/O.
- Implements TTL-based cache invalidation (1 hour).
- Enables real-time validation and enrichment without repeated disk/API calls.

### 4. **Amazon SQS** – *Priority Event Queue*

- Decouples Lambda ingestion from processing logic.
- Two queues: `moving` and `idle` to prioritize `engine_status="moving"` events.
- Enables parallel consumption and ordered priority handling.
- Supports Dead Letter Queue (DLQ) for failed messages and retry logic.

### 5. **AWS Lambda (Consumer)** – *SQS Worker*

- Processes messages from both priority queues.
- Validates speed using Redis metadata.
- Calculates `distance_from_depot` using Haversine formula.
- Deduplicates data using an in-memory Bloom Filter.
- Performs batched writes to DynamoDB.

### 6. **Amazon DynamoDB** – *Telemetry Store*

- Stores telemetry data in a write-optimized, serverless NoSQL table.
- Uses partition key: `vehicle_id`, and sort key: `timestamp`.
- Enables low-latency read/write with scalable throughput and TTL support.
- Supports batch writes to reduce API cost.

### 7. **Dead Letter Queue (DLQ)** – *Failure Tracking*

- Captures unprocessed or failed messages from SQS after 3 retry attempts.
- Enables auditing and custom reprocessing via `dlq_handler.py`.

### 8. **Amazon CloudWatch** – *Observability and Scaling*

- Logs all Lambda execution details and errors.
- Publishes custom metrics (e.g., queue depth, function duration).
- Enables auto-scaling of Lambda concurrency based on SQS metrics.

---

## Optimizations

- All transformations are performed lazily via generators to reduce memory footprint.
- Redis pipelining is used for efficient batch metadata retrieval (future optimization).
- Deduplication is done via Bloom filter to avoid DynamoDB writes for duplicates.
- Parquet format is planned for archived data to improve compression and long-term storage cost.

---

## Cost and Scalability Considerations

- All services are serverless and scale automatically.
- DynamoDB and Lambda are configured for on-demand scaling.
- S3 lifecycle policies manage cost-efficient archival.
- Priority SQS queues ensure latency-sensitive data is processed first.
- Redis minimizes repeated metadata parsing or network I/O.

---

## Fault Tolerance

- Retry logic with exponential backoff is built into SQS + Lambda.
- DLQ tracks errors with full context for recovery or analysis.
- `dlq_handler.py` enables reprocessing of failed messages.
