import json
from aws_xray_sdk.core import xray_recorder


@xray_recorder.capture('response hello decorator')
def hello(event, context):
    # subsegment = xray_recorder.begin_subsegment('subsegment_name')

    body = {
        "message": "Hello!",
    }

    status_code = 200

    response = {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

    # subsegment.put_metadata('key', dict, 'namespace')
    # subsegment.put_annotation('response_status_code', status_code)
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation('response_status_code', status_code)

    return response
