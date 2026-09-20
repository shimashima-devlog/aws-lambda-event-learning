import json
import os
import sys
from unittest.mock import MagicMock

mock_lambda_client = MagicMock()

mock_boto3 = MagicMock()
mock_boto3.client.return_value = mock_lambda_client

sys.modules["boto3"] = mock_boto3

from file_event_handler import lambda_function as event_handler
from file_metadata_builder import lambda_function as metadata_builder
from learning_log_writer import lambda_function as log_writer

os.environ["METADATA_FUNCTION_NAME"] = "local-metadata-builder"
os.environ["LOG_WRITER_FUNCTION_NAME"] = "local-log-writer"

fake_s3_event = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": "local-learning-bucket"
                },
                "object": {
                    "key": "uploads/study/sample.txt"
                }
            }
        }
    ]
}


def fake_invoke(FunctionName, InvocationType, Payload):
    print(f"[LOCAL TEST] Invoke: {FunctionName}")

    payload_data = json.loads(Payload.decode("utf-8"))

    if FunctionName == "local-metadata-builder":
        metadata_builder.lambda_handler(payload_data, None)
        return {"StatusCode": 202}

    if FunctionName == "local-log-writer":
        log_writer.lambda_handler(payload_data, None)
        return {"StatusCode": 202}

    raise ValueError(f"Unknown local function: {FunctionName}")


mock_lambda_client.invoke.side_effect = fake_invoke


if __name__ == "__main__":
    print("=== Local Lambda Flow Test Start ===")

    result = event_handler.lambda_handler(fake_s3_event, None)

    print("=== Local Lambda Flow Test End ===")
    print(result)