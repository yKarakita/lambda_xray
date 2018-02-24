import uuid
import os

import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

patch(['boto3'])

s3_client = boto3.client('s3')

bucket_name = os.environ['S3_BUCKET']


@xray_recorder.capture('put_s3_handler')
def handler(event, context):
    subscribed_data = event['Records'][0]['Sns']
    body = subscribed_data['Message']

    put_object_into_s3(bucket_name, str(uuid.uuid4()), body)

@xray_recorder.capture('put_object')
def put_object_into_s3(bucket_name, bucket_key, body):
    subsegment = xray_recorder.current_subsegment()
    response = s3_client.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    subsegment.put_annotation('put_response', status_code)
