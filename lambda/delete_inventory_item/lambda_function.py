# Testing 
import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON in request body")
        }

    item_id = body.get('item_id')
    item_location_id = body.get('item_location_id')

    if not item_id or item_location_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'item_id' or 'item_location_id' in request body")
        }

    key = {
        'item_id': {'S': item_id},
        'item_location_id': {'N': str(item_location_id)}
    }

    try:
        dynamo_client.delete_item(TableName=table_name, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {item_id} deleted successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
