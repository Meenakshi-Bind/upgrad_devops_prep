import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartChairData')

def lambda_handler(event, context):
    print("Received SQS event:", event)

    try:
        for record in event['Records']:
            data = json.loads(record['body'])
            table.put_item(Item=data)

        return {
            "statusCode": 200,
            "body": json.dumps("Stored successfully in DynamoDB")
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }