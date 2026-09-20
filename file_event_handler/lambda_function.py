import json
import os
import boto3

lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    print(event)

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    file_info = {
        "bucket_name": bucket_name,
        "object_key": object_key
    }

    response = lambda_client.invoke(
        FunctionName=os.environ["METADATA_FUNCTION_NAME"],
        InvocationType="Event",
        Payload=json.dumps(file_info).encode("utf-8")
    )

    print(f"Invoke StatusCode: {response['StatusCode']}")

    return {
        "message": "File event forwarded"
    }