import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    try:
        response = table.scan()
        items = response.get('Items', [])

        for item in items:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    if value % 1 == 0:
                        item[key] = int(value)
                    else:
                        item[key] = float(value)

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving items: {str(e)}")
        }
