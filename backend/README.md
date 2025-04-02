# AI Hiring Take-Home Task

## Overview
This repository contains the solution for the Backend Developer Take-Home task, which involves designing a memory-efficient, serverless pipeline to process high-volume GPS telemetry data for delivery vehicles. The task uses AWS serverless services and Python to ensure scalability, low-latency processing, and cost optimization.

## Key Features
- **Data Ingestion**: Generates and processes telemetry data in chunks.
- **Validation**: Validates records using metadata cached in Redis.
- **Priority Queueing**: Implements priority SQS queues based on `engine_status`.
- **Mock AWS Services**: Uses LocalStack for local development and testing.

## Technologies Used
- **Python**: For data processing and validation.
- **AWS Lambda**: Serverless compute for processing events.
- **AWS SQS**: Queue system for message handling.
- **AWS Redis (ElastiCache)**: For caching vehicle metadata.
- **LocalStack**: For simulating AWS services locally.

## Setup Instructions
1. **Install dependencies**: Run `pip install -r requirements.txt` to install all necessary Python packages.
2. **Start LocalStack**: Use `localstack start` to start the local AWS environment.
3. **Run Redis**: Ensure Redis is running, or start it using `redis-server`.
4. **Generate Data**: Run `python app/scripts/generate_csv_data.py` to generate telemetry data.
5. **Run the Processor**: Execute `python app/scripts/process_csv_stream.py` to process and validate the data.
6. **Run Publisher**: Execute `python app/services/sqs_publisher.py` to publish data to SQS queues.

## Testing
- **LocalStack** is used for local testing of AWS services (SQS, DynamoDB, etc.).
- **Redis** is used to cache metadata for fast validation.

## Conclusion
The pipeline is designed to handle large volumes of data with minimal memory usage and optimized processing using AWS serverless services.
