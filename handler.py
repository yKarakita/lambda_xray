import json
import uuid

from aws_xray_sdk.core import xray_recorder


@xray_recorder.capture('response hello')
def hello(event, context):

    body = {
        "message": "Hello!",
    }

    status_code = 200

    response = {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation('response_status_code', status_code)

    subsegment.put_metadata('key01', {'id': str(uuid.uuid4())}, 'namespace01')
    subsegment.put_metadata('key02', {'id': str(uuid.uuid4())}, 'namespace01')

    return response
