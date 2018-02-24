import json
import os

import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

patch(['boto3'])

sns = boto3.resource('sns', 'ap-northeast-1')
sns_client = boto3.client('sns')

topic_arn = os.environ['SNS_TOPIC_ARN']

@xray_recorder.capture('handler')
def hello(event, context):
    keyword = event['queryStringParameters']['keyword']

    sns_client.publish(
        TopicArn=topic_arn,
        Message=keyword,
        Subject='object_body'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({'message': 'ok'})
    }

    return response
