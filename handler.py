import json
from aws_xray_sdk.core import xray_recorder


def hello(event, context):
    # subsegment = xray_recorder.begin_subsegment('subsegment_name')
    xray_recorder.begin_subsegment('response hello')

    body = {
        "message": "Hello!",
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    # subsegment.put_metadata('key', dict, 'namespace')
    # subsegment.put_annotation('key', 'value')

    xray_recorder.end_subsegment()

    return response
