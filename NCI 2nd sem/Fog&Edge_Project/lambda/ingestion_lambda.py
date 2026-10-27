import json
import boto3
import os

sqs = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/298673434635/smartchair-queue'
def lambda_handler(event, context):
    print("Received event:", event)

    try:
        body = json.loads(event['body'])

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )

        return {
            'statusCode': 200,
            'body': json.dumps("Queued successfully")
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }