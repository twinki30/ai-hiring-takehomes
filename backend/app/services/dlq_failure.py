import boto3
import json

dlq_url = "http://localhost:4566/000000000000/dlq-queue"
sqs = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://localhost:4566")

def reprocess_dlq_messages():
    messages = sqs.receive_message(QueueUrl=dlq_url, MaxNumberOfMessages=10).get("Messages", [])
    for msg in messages:
        try:
            body = json.loads(msg["Body"])
            # Here you would re-invoke the lambda or directly process it
            print(f"Reprocessing: {body}")
            sqs.delete_message(QueueUrl=dlq_url, ReceiptHandle=msg["ReceiptHandle"])
        except Exception as e:
            print(f"Error reprocessing message: {e}")

if __name__ == "__main__":
    reprocess_dlq_messages()
