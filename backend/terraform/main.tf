provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
  endpoint   = "http://localhost:4566"  # LocalStack endpoint
}

resource "aws_lambda_function" "lambda_handler" {
  filename         = "lambda_handler.zip"
  function_name    = "lambda_handler_function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.8"

  environment {
    variables = {
      DYNAMODB_TABLE = "TelemetryData"
      SQS_QUEUE_URL  = aws_sqs_queue.moving_queue.url
      REDIS_HOST     = "localhost"  # Use LocalStack for Redis
      REDIS_PORT     = 6379
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect    = "Allow"
        Sid       = ""
      },
    ]
  })
}

resource "aws_sqs_queue" "moving_queue" {
  name = "moving-queue"
}

resource "aws_dynamodb_table" "telemetry_data" {
  name           = "TelemetryData"
  hash_key       = "vehicle_id"
  range_key      = "timestamp"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "vehicle_id"
    type = "S"
  }
  attribute {
    name = "timestamp"
    type = "S"
  }
}

resource "aws_security_group" "redis_sg" {
  name_prefix = "redis_sg"
}

resource "localstack_dynamodb_table" "telemetry_data" {
  table_name = "TelemetryData"
  hash_key   = "vehicle_id"
  range_key  = "timestamp"
}
