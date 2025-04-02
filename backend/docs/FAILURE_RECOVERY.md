# FAILURE_RECOVERY.md

## Overview
This document outlines the failure recovery strategy for handling errors and reprocessing messages in a serverless pipeline designed to process high-volume geospatial telemetry data. The system utilizes AWS services such as Lambda, SQS, DynamoDB, and Redis, and must handle various failure scenarios, including failures during processing, retries, and dead-letter queue management.

## 1. Reprocessing Failed Messages from Dead Letter Queue (DLQ)

### Scenario: Message Processing Failure
When Lambda functions fail to process a message (e.g., invalid data, failed integration with external services), the message is sent to a Dead Letter Queue (DLQ) for further inspection and reprocessing.

### Step-by-Step Recovery Process

1. **Identify Failed Messages:**
   - Monitor the DLQ for new messages.
   - Use AWS CloudWatch Logs to check Lambda errors and identify which messages failed.

2. **Analyze the Message:**
   - Retrieve the message from the DLQ.
   - Investigate the error by analyzing the message body and logs associated with the failure.
   - Common failures might include missing metadata or invalid data.

3. **Reprocessing Failed Messages:**
   - Once the root cause of the failure is identified and fixed, manually or automatically trigger the reprocessing of the failed message.
   - For instance, if the failure was due to missing metadata, load the metadata into Redis and re-invoke the Lambda function with the corrected data.

4. **Retry Logic for SQS Messages:**
   - For failed SQS messages that have not yet reached the DLQ:
     - Configure SQS message retry logic with a maximum retry count of 3.
     - Ensure the retry policy is backoff-based (e.g., exponential backoff) to avoid overloading the system.

### Code Example for Retrieving and Reprocessing from DLQ

```python
import boto3
import json

sqs = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')
dlq_url = "http://localhost:4566/000000000000/dead-letter-queue"

def process_dlq_messages():
    # Retrieve messages from the DLQ
    response = sqs.receive_message(
        QueueUrl=dlq_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=30,  # Prevent other consumers from processing while handling
        WaitTimeSeconds=20
    )
    
    if 'Messages' in response:
        for message in response['Messages']:
            try:
                message_body = json.loads(message['Body'])
                # Reprocess message logic
                process_message(message_body)
                
                # Delete the message from DLQ after successful processing
                sqs.delete_message(
                    QueueUrl=dlq_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            except Exception as e:
                print(f"Error processing DLQ message {message['MessageId']}: {e}")
    else:
        print("No messages in DLQ to process.")

def process_message(message):
    # Simulate processing of the message
    print(f"Reprocessing message: {message}")
    # Example of reprocessing logic (e.g., validate, process, and send to another SQS queue)
    publish_to_sqs(message)
