import json
import os
import boto3

lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    print(event)

    bucket_name = event["bucket_name"]
    object_key = event["object_key"]

    file_name = os.path.basename(object_key)
    file_extension = os.path.splitext(file_name)[1]

    metadata = {
        "bucket_name": bucket_name,
        "object_key": object_key,
        "file_name": file_name,
        "file_extension": file_extension
    }

    response = lambda_client.invoke(
        FunctionName=os.environ["LOG_WRITER_FUNCTION_NAME"],
        InvocationType="Event",
        Payload=json.dumps(metadata).encode("utf-8")
    )

    print(f"Invoke StatusCode: {response['StatusCode']}")

    return {
        "message": "File metadata forwarded"
    }