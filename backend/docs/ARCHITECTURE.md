# ARCHITECTURE.md

## Overview
This document outlines the high-level architecture for a memory-efficient, serverless pipeline that ingests and processes high-volume GPS telemetry data from over 50,000 delivery vehicles. The architecture is built using AWS serverless components with scalability, low-latency, and cost-optimization as primary goals.

## Architecture Diagram


## Key Requirements
- **Data Volume**: 1M+ telemetry events/day
- **Latency Target**: Sub-second for ingestion and queueing
- **Memory Constraint**: ≤512MB per Lambda function
- **Tech Stack**: Python, AWS Lambda, S3, SQS, DynamoDB, Redis (ElastiCache), Terraform

## Architecture Components & Rationale

### 1. **Data Ingestion Layer**
- **Amazon S3**: Stores raw CSV telemetry files uploaded periodically or in real time.
- **Trigger**: S3 Event Notification to Lambda
- **Justification**: S3 provides durable, cost-effective storage; event-based trigger enables real-time processing.

### 2. **Stream Processor (Lambda Function)**
- **Function**: Reads and processes the uploaded CSV files in chunks (≤100MB).
- **Validation**:
  - Discard invalid records (e.g., `lat > 90`, `speed > max_speed`)
  - Cache metadata using Redis for fast validation.
- **Justification**: Lambda enables scalable, stateless processing. Chunked streaming ensures memory efficiency under 512MB.
- **Architecture Note**: Two Lambda functions are used—one for S3 ingestion, one for SQS processing. This separation improves failure isolation and independent scaling.

### 3. **Caching Layer**
- **Redis (ElastiCache)**: Stores vehicle metadata from `metadata_api.json`
- **TTL**: 1 hour for cache invalidation
- **Justification**: Reduces latency and cost by avoiding repeated metadata lookups. TTL ensures updated data is used.

### 4. **Queueing Layer**
- **Amazon SQS (Standard + FIFO Queues)**:
  - Priority queueing: Events with `engine_status = 'moving'` prioritized over `idle`
  - DLQ (Dead Letter Queue) for failed messages
- **Justification**: Decouples processing, adds fault tolerance, supports retries, and prioritization via queue separation.

### 5. **Storage & Processing Layer**
- **Amazon DynamoDB**:
  - Stores telemetry events indexed by `vehicle_id` + `timestamp`
  - Uses batch writes for cost efficiency
  - Optional TTL for storage cost reduction
- **Distance Calculation**:
  - Compute `distance_from_depot` using Haversine formula in a memory-safe way (via `generators`)
- **Justification**: DynamoDB provides scalable, low-latency storage with fine-grained throughput control.

### 6. **Failure Recovery**
- **DLQ with Metadata**: Captures errors and metadata for triaging
- **Retry Logic**: Max 3 retries, configured via Lambda retry policies and SQS redrive policies
- **Justification**: Enables observability, alerting, and manual reprocessing.

### 7. **Observability & Monitoring**
- **Amazon CloudWatch**:
  - Custom metrics (latency, memory usage, DLQ depth)
  - Dashboards and alerts for queue length, Lambda errors
- **Justification**: Provides real-time visibility into system health and performance.

### 8. **Scalability & Cost Optimization**
- **Lambda Auto-scaling**:
  - Based on SQS queue depth using CloudWatch alarms + Lambda concurrency limits
- **S3 Lifecycle Rules**:
  - Transition to Glacier after 7 days for archival
- **Parquet Conversion**:
  - Compress and convert raw data to Parquet format for long-term storage
- **Deduplication Strategy**:
  - Use Bloom filters to avoid storing duplicate records (vehicle_id + timestamp)

### 9. **Security & Access Control**
- **IAM Roles and Policies**:
  - Minimal access roles for each Lambda function (e.g., read-only for S3, write-only for DynamoDB)
  - Secure Redis with IAM auth or VPC Security Groups
- **Justification**: Implements least-privilege access to ensure secure operations.

### 10. **Local Development & Testing**
- **Moto / LocalStack**:
  - Used to mock AWS services for local development and automated testing
- **Justification**: Enables testing without requiring live AWS infrastructure

---

## Summary of Technologies

| Component           | AWS Service     | Purpose                                 |
|--------------------|------------------|------------------------------------------|
| File Storage        | S3               | Raw telemetry CSV files                  |
| Compute             | Lambda           | Serverless processing                    |
| Message Queue       | SQS              | Decoupling and prioritization            |
| Caching             | Redis            | Fast metadata access                     |
| Database            | DynamoDB         | Telemetry data storage                   |
| Monitoring          | CloudWatch       | Observability and auto-scaling triggers  |
| Archival Storage    | S3 + Glacier     | Cost-optimized historical data retention |

---

## Next Steps
- [ ] Finalize `process_csv_stream.py` with chunked processing
- [ ] Implement Redis caching and metadata loader
- [ ] Setup DynamoDB batch writes and deduplication logic
- [ ] Write Terraform templates for provisioning AWS infrastructure
- [ ] Populate TRADEOFFS.md, PERFORMANCE.md, and FAILURE_RECOVERY.md

---

For any questions or improvements, refer to `L2.md` and project README.
