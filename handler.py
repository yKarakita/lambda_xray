import json
import uuid
import boto3
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

patch(['boto3'])

s3_client = boto3.client('s3')

bucket_name = os.environ['S3_BUCKET']


@xray_recorder.capture('response hello')
def hello(event, context):
    body = event['queryStringParameters']['keyword']

    put_object_into_s3(bucket_name, str(uuid.uuid4()), body)

    response = {
        "statusCode": 200,
        "body": json.dumps({'message': 'ok'})
    }

    return response


@xray_recorder.capture('put_object')
def put_object_into_s3(bucket_name, bucket_key, body):
    subsegment = xray_recorder.current_subsegment()
    response = s3_client.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    subsegment.put_annotation('put_response', status_code)
