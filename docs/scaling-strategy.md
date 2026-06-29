# LogiHaul Scaling Strategy

## Overview

LogiHaul is designed to support unpredictable traffic increases of up to 50× during events such as promotions, peak delivery periods, or flood-related demand.

The scaling strategy combines infrastructure scaling, managed database scaling, and serverless concurrency to ensure that order processing remains available while controlling infrastructure cost.

The architecture uses:

- Amazon EC2 Auto Scaling Group for application compute scaling
- DynamoDB On-Demand capacity for automatic database scaling
- AWS Lambda concurrency for event processing scalability
- Amazon SQS for workload buffering during spikes
- Amazon ElastiCache Redis for reducing database pressure

---

# 1. Compute Scaling — EC2 Auto Scaling Group

## Strategy

The web application layer runs on EC2 instances behind an Application Load Balancer.

The EC2 instances are managed by an Auto Scaling Group configured with:

- Minimum capacity: 1 instance
- Desired capacity: 1 instance
- Maximum capacity: 3 instances

## Normal Traffic

During normal operations, the ASG maintains the minimum required number of EC2 instances to reduce infrastructure cost.

The Application Load Balancer routes incoming user requests to healthy application servers.

## 50× Traffic Spike Handling

During promotions or flood events, request volume may increase significantly.

The Auto Scaling Group monitors application metrics through CloudWatch.

When demand increases beyond the configured threshold, the ASG launches additional EC2 instances.

The Application Load Balancer automatically distributes incoming traffic across the new healthy instances.

This allows LogiHaul to increase application capacity without manually provisioning servers.

---

# 2. Database Scaling — DynamoDB

## Strategy

DynamoDB was configured using On-Demand capacity mode.

## Reason

LogiHaul has unpredictable order creation patterns where traffic can increase suddenly.

Provisioned capacity would require estimating future traffic and manually adjusting read/write capacity.

On-Demand capacity allows DynamoDB to automatically scale request handling based on actual workload demand.

## 50× Traffic Spike Handling

During a traffic spike:

- More customers submit orders
- Lambda 1 creates more DynamoDB write operations
- DynamoDB automatically adjusts capacity to handle increased request volume

This prevents database capacity planning from becoming a bottleneck during unpredictable demand.

---

# 3. Serverless Scaling — Lambda Concurrency

## Strategy

Lambda functions automatically scale by creating additional execution environments when invocation requests increase.

LogiHaul uses two Lambda functions with separate responsibilities:

## Lambda 1 — Order Processor

Handles:

- API requests
- Request validation
- DynamoDB writes
- Sending messages to SQS

During a spike, Lambda 1 can process multiple order requests concurrently rather than handling requests sequentially.

This allows order creation to remain responsive.

## Lambda 2 — Notification Processor

Handles:

- Reading messages from SQS
- Formatting notifications
- Publishing to SNS

Lambda 2 scales independently based on the number of messages waiting in SQS.

This prevents notification workload increases from affecting customer order processing.

---

# 4. SQS Buffering Strategy

## Strategy

Amazon SQS is used as a decoupling layer between order processing and notifications.

## 50× Traffic Spike Handling

During a large increase in orders:

Lambda 1 continues processing customer requests.

Instead of waiting for notification delivery, notification tasks are stored in SQS.

The queue absorbs sudden increases in workload and allows Lambda 2 to process messages at its own pace.

This prevents downstream notification failures from impacting order placement.

---

# 5. Redis Performance Scaling

## Strategy

Redis is used as a caching layer to reduce repeated database queries.

## 50× Traffic Spike Handling

During high traffic periods, repeated requests such as:

- Delivery status checks
- Order tracking requests

can be served from Redis instead of repeatedly querying RDS.

This reduces database load and improves response times.

The cache-aside approach allows the application to maintain performance while database demand increases.

---

# Scaling Summary

| Component | Scaling Method | Purpose |
|---|---|---|
| EC2 | Auto Scaling Group | Increase web application capacity |
| ALB | Traffic distribution | Route requests to healthy servers |
| DynamoDB | On-Demand capacity | Handle unpredictable order writes |
| Lambda | Concurrent executions | Process events in parallel |
| SQS | Queue buffering | Absorb workload spikes |
| Redis | Caching | Reduce database pressure |

---

# Future Production Scaling Improvements

For larger production workloads, LogiHaul can further improve scalability by:

- Increasing ASG maximum capacity
- Adding predictive scaling policies
- Introducing Multi-AZ RDS deployment
- Adding Redis replication
- Implementing infrastructure monitoring-based scaling
- Introducing CDN caching for static content

The scaling strategy ensures that LogiHaul can handle unpredictable traffic growth while maintaining reliability, performance, and cost efficiency.