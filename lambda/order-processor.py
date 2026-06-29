import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

TABLE_NAME = os.environ["TABLE_NAME"]
QUEUE_URL = os.environ["QUEUE_URL"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    print("EVENT RECEIVED:")
    print(json.dumps(event))

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    order = {
        "order_id": body["order_id"],
        "customer_name": body["customer_name"],
        "customer_phone": body["customer_phone"],
        "pickup_location": body["pickup_location"],
        "delivery_location": body["delivery_location"],
        "order_status": body["order_status"],
        "order_timestamp": body.get(
            "order_timestamp",
            datetime.utcnow().isoformat()
        ),
        "driver_id": body.get("driver_id", "Unassigned"),
        "delivery_fee": body["delivery_fee"],
        "payment_status": body["payment_status"]
    }

    table.put_item(
        Item=order
    )

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(order)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order created successfully",
            "order_id": order["order_id"]
        })
    }