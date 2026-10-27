terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.76.0"
    }
  }
  backend "s3" {
    bucket = "terraform-fog-and-edge"
    key    = "terraformfile/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  # Configuration options
  region = "us-east-1"
}

# ------------------------
# DynamoDB Table
# ------------------------
resource "aws_dynamodb_table" "smartchair" {
  name         = "SmartChairData"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "chair_id"
  range_key    = "timestamp"

  attribute {
    name = "chair_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }
}

# ------------------------
# SQS Queue
# ------------------------
resource "aws_sqs_queue" "smartchair_queue" {
  name = "smartchair-queue"
}

# ------------------------
# Use Existing LabRole
# ------------------------
data "aws_iam_role" "labrole" {
  name = "LabRole"
}

# ------------------------
# Lambda Functions
# ------------------------
resource "aws_lambda_function" "ingestion" {
  function_name = "SmartChairIngestion"
  role          = data.aws_iam_role.labrole.arn
  handler       = "ingestion_lambda.lambda_handler"
  runtime       = "python 3.14"

  filename = "lambda/ingestion_lambda.zip"
}

resource "aws_lambda_function" "processor" {
  function_name = "SmartChairProcessor"
  role          = data.aws_iam_role.labrole.arn
  handler       = "processor_lambda.lambda_handler"
  runtime       = "python 3.14"

  filename = "lambda/processor_lambda.zip"
}

# ------------------------
# SQS → Lambda Trigger
# ------------------------
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.smartchair_queue.arn
  function_name    = aws_lambda_function.processor.arn
}

# ------------------------
# API Gateway HTTP API
# ------------------------
resource "aws_apigatewayv2_api" "api" {
  name          = "smartchair-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "integration" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.ingestion.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /chairdata"
  target    = "integrations/${aws_apigatewayv2_integration.integration.id}"
}

resource "aws_apigatewayv2_stage" "stage" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

# ------------------------
#  API Gateway → Lambda
# ------------------------
resource "aws_lambda_permission" "apigw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestion.function_name
  principal     = "apigateway.amazonaws.com"
}