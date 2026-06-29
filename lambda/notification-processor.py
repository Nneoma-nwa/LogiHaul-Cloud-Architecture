import json
import boto3
import os

sns = boto3.client("sns")

TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):

    for record in event["Records"]:

        order = json.loads(record["body"])

        message = f"""
Hello {order['customer_name']},

Thank you for your order with LogiHaul. We have successfully received your delivery request and our team is processing it.

Order Details:
--------------------------------
Order ID: {order['order_id']}
Delivery Location: {order['delivery_location']}
Order Status: {order['order_status']}
Payment Status: {order['payment_status']}
--------------------------------

We will keep you updated as your delivery progresses.

Thank you for choosing LogiHaul. We appreciate your trust and look forward to delivering a great experience.

Best regards,
LogiHaul Delivery Team
"""

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="LogiHaul Order Update",
            Message=message
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Notification sent successfully"
            }
        )
    }