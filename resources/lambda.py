import json
import os
import boto3
from datetime import datetime
import string
import random


dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
ID_LENGTH = os.environ['ID_LENGTH']


def short_url(event, context):

    payload = json.loads(event['body'])
    rand_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=int(ID_LENGTH)))
    data = {
            'id': rand_id,
            'url': payload['url'],
            'created_date': datetime.utcnow().isoformat(),
            'ip': event['requestContext']['identity']['sourceIp'],
            'country': event['headers']['CloudFront-Viewer-Country']
        }

    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.put_item(Item=data)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': data
    }


def read_url(event, context):

    rand_id = event['pathParameters']['randId']
    keys = {
            'id': rand_id,
        }

    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.get_item(Key=keys)

    if response.get('Item'):

        return {
            'statusCode': 302,
            'headers': {
                'Location': response['Item']['url']
            }
        }

    return {
        'statusCode': 404
    }