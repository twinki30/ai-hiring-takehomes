# TRADEOFFS.md

## SQS vs Kinesis
**SQS:**
- **Pros:**
  - Simple to use and configure.
  - Built-in message durability and retries.
  - Supports message batching, which is useful for high throughput.
  - Provides dead-letter queues for failed message processing.
  - Can integrate seamlessly with AWS Lambda for event-driven processing.

- **Cons:**
  - Limited message size (up to 256 KB).
  - Does not provide event stream processing out of the box, which might be required for real-time analytics.

**Kinesis:**
- **Pros:**
  - Real-time event stream processing, which is ideal for high-frequency telemetry data.
  - High throughput and scalability, can handle millions of records per second.
  - Supports real-time data analytics with Kinesis Data Analytics.
  - Ideal for use cases requiring continuous event stream processing and analytics.

- **Cons:**
  - Slightly more complex to manage compared to SQS.
  - Higher cost at high throughput levels.
  - No built-in dead-letter queue (DLQ) support.

**Decision:**
- **SQS** is chosen for simplicity and cost-effectiveness, particularly for decoupling producers/consumers in this scenario. Since the pipeline focuses on event processing rather than continuous analytics, SQS is sufficient to handle the telemetry data.

---

## DynamoDB vs RDS
**DynamoDB:**
- **Pros:**
  - Fully managed, serverless, and scales automatically.
  - Low-latency reads and writes.
  - Best suited for high-velocity, high-frequency access patterns (like telemetry data).
  - Supports DynamoDB Streams, which can trigger Lambda functions.
  - No need to manage instances or database backups.

- **Cons:**
  - Limited query capabilities compared to relational databases.
  - Requires schema design for high availability and scaling (e.g., partition keys).
  - Expensive at high throughput rates.

**RDS (Relational Database Service):**
- **Pros:**
  - Supports relational schema, which can be beneficial for complex queries.
  - Managed solution that supports MySQL, PostgreSQL, etc.
  - Advanced querying capabilities.

- **Cons:**
  - Requires more management compared to DynamoDB.
  - Not designed for high-velocity workloads like telemetry data.
  - Scaling can become more complex and costly at large scales.

**Decision:**
- **DynamoDB** is chosen because it provides scalable, low-latency access to telemetry data. The data structure is simple and doesn’t require complex joins, making DynamoDB an ideal solution for high-velocity workloads.

---

## Lambda Concurrency Scaling
**Auto-scaling Lambda Concurrency:**
- **Pros:**
  - Automatically scales Lambda functions based on the number of events in the SQS queue.
  - Reduces operational overhead as AWS manages scaling.
  - Ensures that telemetry events are processed in near real-time without manual intervention.

- **Cons:**
  - Can lead to cold start latencies if the Lambda function is not invoked frequently enough.
  - High scaling during peak times can result in increased costs.
  - If not properly tuned, it can lead to throttling or excessive invocations.

**Decision:**
- **Auto-scaling Lambda concurrency** is chosen for its simplicity and the ability to scale the event processing dynamically based on queue depth. This is ideal for handling fluctuating telemetry data volumes.

---

## S3 vs Glacier for Telemetry Data Storage
**S3 (Standard Storage Class):**
- **Pros:**
  - Fast and frequent access to the stored data.
  - Provides high durability (11 nines of durability).
  - Easy integration with Lambda, CloudWatch, and other AWS services.

- **Cons:**
  - Higher storage cost compared to Glacier for archival data.
  - Not ideal for long-term storage of infrequently accessed data.

**Glacier:**
- **Pros:**
  - Much cheaper storage for infrequently accessed data.
  - Can store large amounts of telemetry data over a long period at lower costs.

- **Cons:**
  - Retrieval times can range from minutes to hours, which is not ideal for real-time access.
  - Retrieval costs can add up if accessed frequently.

**Decision:**
- **S3 (Standard)** is used for real-time telemetry data, and **Glacier** is used for storing older data. A tiered storage model allows for cost-effective data management while ensuring real-time access for active telemetry data.

---

## Memory-Safe Transformations Using Generators
**Generators vs Lists:**
- **Generators:**
  - **Pros:** 
    - Efficient memory usage, as data is yielded one item at a time rather than being loaded into memory all at once.
    - Ideal for processing large files, especially when dealing with huge telemetry datasets.
  
  - **Cons:**
    - No random access to elements; they must be consumed in order.

- **Lists:**
  - **Pros:**
    - Provide fast, random access to data.
    - Simpler to implement for small datasets or when needing to perform multiple operations on data.

  - **Cons:**
    - Memory-intensive for large datasets, potentially leading to memory overflow errors.
  
**Decision:**
- **Generators** are used for memory-safe transformations of telemetry data to avoid memory overload when processing large datasets, ensuring the pipeline can scale to 1M+ daily events.

---

## Cost-Optimized Storage and Conversion to Parquet
**Parquet vs CSV:**
- **Parquet:**
  - **Pros:**
    - Columnar storage format, ideal for storing large amounts of data that require efficient reads and compression.
    - Significant storage savings due to compression (up to 75% smaller than CSV).
    - Optimized for analytics and querying with tools like AWS Athena.

  - **Cons:**
    - Requires more complex setup for writing and reading (i.e., requires schema definition).
  
- **CSV:**
  - **Pros:**
    - Simple and widely supported format.
    - Ideal for basic data processing without the need for complex setups.

  - **Cons:**
    - High storage costs for large volumes of data due to lack of compression.
    - Inefficient for querying and analysis, as the entire file needs to be read into memory.

**Decision:**
- **Parquet** is chosen for archival storage in S3 to save on storage costs and enable faster querying when accessing older data.

---

## Bloom Filters for Deduplication
**Bloom Filter:**
- **Pros:**
  - Very efficient in terms of space for storing large sets of data.
  - Allows checking if an element is in a set without storing all the data.
  - No false positives, but allows for occasional false negatives.

- **Cons:**
  - Once an element is added, it cannot be removed.
  - May require tuning of the size and error rate for the filter to be effective.

**Decision:**
- A **Bloom filter** is used to deduplicate telemetry data, ensuring that only unique vehicle and timestamp combinations are processed without storing the entire data set, thus reducing memory usage.

---

# Conclusion
The architecture and technologies chosen prioritize cost-effectiveness, memory efficiency, and scalability. SQS is used for message queuing, DynamoDB for scalable data storage, and Redis for caching metadata. The use of Lambda with auto-scaling ensures the system can handle a large volume of telemetry data, while Bloom filters and Parquet provide efficient data processing and storage.
