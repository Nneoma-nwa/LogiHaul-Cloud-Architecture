# LogiHaul Architecture Tradeoffs

## Overview

The LogiHaul architecture was designed by balancing scalability, availability, security, operational complexity, and cost.

Because the platform is expected to support nationwide logistics operations with unpredictable traffic spikes, every architectural choice involved evaluating the tradeoff between immediate business needs and future production requirements.

The implementation intentionally avoids unnecessary complexity while maintaining a clear migration path toward a highly available production architecture.

---

# 1. Single NAT Gateway vs Multi-AZ NAT Gateway

## Decision

A single NAT Gateway was deployed in one public subnet.

## Alternative Considered

Deploying a NAT Gateway in each Availability Zone.

## Tradeoff

A multi-AZ NAT Gateway architecture provides stronger availability because private resources in each Availability Zone have their own outbound internet path.

However, NAT Gateways introduce additional monthly cost.

For the current LogiHaul deployment stage, a single NAT Gateway provides the required outbound connectivity while reducing infrastructure cost.

The limitation is that if the Availability Zone hosting the NAT Gateway becomes unavailable, private subnet resources relying on that NAT Gateway may lose outbound internet access.

Future production improvements:

- Deploy one NAT Gateway per Availability Zone
- Update private subnet route tables accordingly

---

# 2. Single-AZ RDS + Read Replica vs Multi-AZ RDS

## Decision

The primary RDS PostgreSQL database was deployed using Single-AZ with a Read Replica.

## Alternative Considered

Multi-AZ RDS deployment.

## Tradeoff

Multi-AZ provides automatic failover and improved database availability.

However, it increases cost because an additional standby database instance is maintained.

The current architecture prioritizes affordability while improving read scalability through a Read Replica.

The Read Replica helps distribute read workloads such as:

- Delivery tracking
- Order history
- Reporting queries

Future production improvements:

- Introduce Multi-AZ for automated failover
- Add additional replicas for higher read throughput

---

# 3. RDS PostgreSQL vs Aurora PostgreSQL

## Decision

Amazon RDS PostgreSQL was selected.

## Alternative Considered

Amazon Aurora PostgreSQL.

## Tradeoff

Aurora provides:

- Higher throughput
- Faster failover
- Distributed storage
- Better scaling capabilities

However, Aurora introduces additional cost and operational complexity.

RDS PostgreSQL provides the required relational database capabilities for:

- Orders
- Driver assignments
- Billing
- Delivery records

For the current workload, RDS provides the best balance between reliability and cost.

Aurora can be introduced when transaction volume and availability requirements increase.

---

# 4. EC2 + Auto Scaling vs Fully Serverless Compute

## Decision

A hybrid architecture using EC2 and serverless services was implemented.

## Alternative Considered

Moving the entire application layer to Lambda.

## Tradeoff

A fully serverless architecture would reduce infrastructure management and automatically scale workloads.

However, the existing web application layer benefits from traditional compute through:

- Persistent application runtime
- Load balancing
- Auto Scaling control
- Easier migration of existing applications

Serverless services were used where they provided the most value:

- API processing
- Event handling
- Notifications

This hybrid approach balances flexibility and operational control.

---

# 5. HTTP API vs REST API

## Decision

API Gateway HTTP API was selected.

## Alternative Considered

API Gateway REST API.

## Tradeoff

REST API provides additional features and deeper API management capabilities.

However, HTTP API provides:

- Lower latency
- Lower cost
- Simpler configuration

For the LogiHaul ordering workflow, HTTP API provides the required functionality without additional overhead.

---

# 6. SQS Decoupling vs Direct Lambda Invocation

## Decision

SQS was placed between order processing and notification processing.

## Alternative Considered

Lambda 1 directly invoking Lambda 2.

## Tradeoff

Direct invocation creates tighter coupling between services.

If notification processing fails, order processing may also be affected.

Using SQS provides:

- Message persistence
- Retry capability
- Failure isolation
- Asynchronous processing

The tradeoff is increased architectural complexity because another service must be managed.

However, the reliability benefits are more important for logistics workflows.

---

# 7. Redis Cache vs Direct Database Access

## Decision

Redis was introduced as a caching layer.

## Alternative Considered

Application reading directly from RDS.

## Tradeoff

Direct database access is simpler and reduces infrastructure components.

However, repeated database queries increase latency and database load.

Redis improves:

- Response time
- Database scalability
- User experience during traffic spikes

The tradeoff is additional operational responsibility for cache management.

---

# 8. On-Demand EC2 vs Reserved Instances

## Decision

On-Demand EC2 pricing was selected.

## Alternative Considered

Reserved Instances.

## Tradeoff

Reserved Instances provide lower long-term cost when workloads are predictable.

However, LogiHaul is still evolving and traffic patterns are not fully established.

On-Demand provides:

- Flexibility
- No long-term commitment
- Easier scaling changes

Reserved Instances can be introduced when production usage becomes stable.

---

# 9. Single Redis Node vs Redis Replication

## Decision

A single Redis node was deployed.

## Alternative Considered

Redis replication with multiple nodes.

## Tradeoff

Replication improves:

- Availability
- Failover capability
- Read scalability

However, it increases cost and configuration complexity.

The current implementation focuses on demonstrating caching capability while keeping infrastructure costs controlled.

Future production deployment should consider Redis replication.

---

# 10. Managed Services vs Self-Managed Infrastructure

## Decision

AWS managed services were used wherever possible.

Examples:

- RDS
- DynamoDB
- SQS
- SNS
- CloudWatch

## Alternative Considered

Self-managed databases, queues, and monitoring systems on EC2.

## Tradeoff

Self-managed systems provide more control but require:

- Server maintenance
- Patching
- Scaling management
- Operational overhead

Managed services reduce operational burden and allow the team to focus on application functionality.

---

# Final Tradeoff Summary

The LogiHaul architecture intentionally chooses simplicity and cost efficiency for the current implementation while preserving a clear path toward production-scale improvements.

Current priorities:

- Secure architecture
- Cost control
- Demonstrated scalability
- Operational simplicity

Future priorities:

- Higher availability
- Multi-AZ database resilience
- Increased fault tolerance
- Advanced scaling strategies