import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON in request body")
        }

    id_value = body.get('id')
    location_id_value = body.get('location_id')

    if not id_value or location_id_value is None:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' in request body")
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Item fetched successfully.",
            "item": {
                "id": id_value,
                "location_id": location_id_value
            }
        })
    }
