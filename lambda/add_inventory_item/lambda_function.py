# Testing
import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON in request body")
        }

    required_fields = [
        'item_id',
        'item_location_id',
        'name',
        'description',
        'qty_on_hand',
        'price'
    ]

    missing_fields = [f for f in required_fields if f not in body]
    if missing_fields:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing required fields: {', '.join(missing_fields)}")
        }

    try:
        item = {
            'item_id': str(body['item_id']),
            'item_location_id': Decimal(str(body['item_location_id'])),
            'name': str(body['name']),
            'description': str(body['description']),
            'qty_on_hand': Decimal(str(body['qty_on_hand'])),
            'price': Decimal(str(body['price']))
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Invalid field types: {str(e)}")
        }

    try:
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Item added successfully.",
                "item": body
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
