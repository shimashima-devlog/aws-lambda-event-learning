import json


def lambda_handler(event, context):
    print("File metadata received")
    print(json.dumps(event, ensure_ascii=False, default=str))

    return {
        "message": "File metadata logged"
    }