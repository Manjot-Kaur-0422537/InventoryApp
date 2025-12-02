### Testing ###
import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
TABLE_NAME = 'Inventory'

def lambda_handler(event, context):
    try:
        body = event  

        action = body.get('action')
        if not action or action not in ['add', 'get']:
            return {
                'statusCode': 400,
                'body': json.dumps("Missing or invalid 'action'. Must be 'add' or 'get'.")
            }

        if action == 'add':
            item_location_id = body.get('item_location_id')
            item_name = body.get('item_name')
            item_description = body.get('item_description')
            item_qty_on_hand = body.get('item_qty_on_hand')
            item_price = body.get('item_price')

            if item_location_id is None or not item_name:
                return {
                    'statusCode': 400,
                    'body': json.dumps("Missing required fields: item_location_id, item_name")
                }

            item_id = str(uuid.uuid4())

            item = {
                'item_id': {'S': item_id},
                'item_location_id': {'N': str(item_location_id)},  # N type
                'item_name': {'S': item_name},
                'item_description': {'S': item_description or "No description"},
                'item_qty_on_hand': {'N': str(item_qty_on_hand or 0)},
                'item_price': {'N': str(item_price or 0)}
            }

            dynamodb.put_item(TableName=TABLE_NAME, Item=item)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Item added successfully',
                    'item_id': item_id
                })
            }

        elif action == 'get':
            item_id = body.get('item_id')
            item_location_id = body.get('item_location_id')

            if not item_id or item_location_id is None:
                return {
                    'statusCode': 400,
                    'body': json.dumps("Missing required fields: item_id, item_location_id")
                }

            key = {
                'item_id': {'S': item_id},
                'item_location_id': {'N': str(item_location_id)}  
            }

            response = dynamodb.get_item(TableName=TABLE_NAME, Key=key)
            item = response.get('Item')

            if not item:
                return {
                    'statusCode': 404,
                    'body': json.dumps("Item not found")
                }

            result = {
                'item_id': item['item_id']['S'],
                'item_location_id': int(item['item_location_id']['N']),
                'item_name': item['item_name']['S'],
                'item_description': item['item_description']['S'],
                'item_qty_on_hand': int(item['item_qty_on_hand']['N']),
                'item_price': float(item['item_price']['N'])
            }

            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"ClientError: {e.response['Error']['Message']}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
