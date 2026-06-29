# Architecture Decisions & Design Rationale

The LogiHaul architecture was designed around the requirements of a nationwide logistics platform operating across 36 states, supporting 5,000 truck drivers and handling unpredictable traffic spikes of up to 50× during promotions and flood events.

Each architectural decision was evaluated based on scalability, availability, security, operational complexity, and cost efficiency.

---

# 1. Foundation & Identity Decisions

## VPC CIDR and Subnet Design

### Decision

A custom VPC using the CIDR block:

**10.0.0.0/16**

was selected.

### Rationale

The **10.0.0.0/16** CIDR block provides 65,536 private IP addresses, giving LogiHaul sufficient address capacity for current workloads and future expansion.

The VPC was divided across two Availability Zones using public and private subnets.

### Public Subnets

The public subnets contain:

- Application Load Balancer (ALB)
- NAT Gateway
- Bastion Host

### Private Subnets

The private subnets contain:

- EC2 application servers
- Amazon RDS PostgreSQL
- Amazon ElastiCache Redis

This design improves security by preventing sensitive resources from being directly accessible from the internet while still allowing controlled communication between application components.

The two Availability Zone design reduces dependency on a single physical location and improves resilience.

---

# NAT Gateway Strategy

## Decision

A single NAT Gateway was deployed.

## Rationale

The NAT Gateway provides outbound internet connectivity for private subnet resources without exposing them publicly.

A multi-AZ NAT Gateway design would provide stronger fault tolerance by deploying a NAT Gateway in each Availability Zone.

However, the initial implementation prioritizes cost optimization because the current workload does not justify the additional monthly expense.

The architecture remains extensible, allowing additional NAT Gateways to be introduced as traffic volume and availability requirements increase.

---

# Security Group Design

## Decision

Security Groups were implemented using least privilege principles.

## Rationale

The application follows a layered security model:

Internet → Application Load Balancer → EC2 Application Servers → Database Layer

Security rules include:

- ALB accepts public HTTP traffic
- EC2 only accepts traffic from ALB
- RDS only accepts database traffic from EC2
- Redis only accepts connections from the application layer
- SSH access is restricted through the Bastion Host

This reduces the attack surface while maintaining controlled administrative access.

---

# 2. Compute & Scaling Decisions

## EC2 Instance Selection

### Decision

**t3.micro On-Demand**

### Rationale

The t3.micro instance type was selected because the LogiHaul web tier requires cost-effective compute suitable for lightweight and variable workloads.

The burstable CPU model allows temporary increases in processing demand without paying for continuously high-performance instances.

On-Demand pricing was selected because the platform is still evolving and workload patterns are not yet predictable.

For a mature production workload with stable usage patterns, Reserved Instances could reduce long-term compute costs.

---

# Application Load Balancer and Auto Scaling

## Decision

A single Application Load Balancer deployed across two Availability Zones was combined with an Auto Scaling Group.

## Rationale

The LogiHaul platform experiences unpredictable traffic spikes, including possible 50× increases during promotions or flood events.

The Application Load Balancer acts as the single entry point for incoming user requests and distributes traffic across healthy EC2 application servers running in the private subnets.

Deploying the ALB across two Availability Zones improves availability by reducing dependency on a single Availability Zone.

The Auto Scaling Group automatically adjusts EC2 capacity based on demand.

This prevents unnecessary infrastructure cost during normal usage while allowing the system to scale during peak periods.
---

# 3. Storage Decisions

## Amazon S3

### Decision

Amazon S3 was used for static website hosting and object storage.

### Rationale

S3 was selected because it provides:

- High durability
- Scalable storage
- Encryption support
- Lifecycle management
- Cross-region replication capability

Versioning protects against accidental deletion or modification.

Lifecycle policies optimize storage cost by transitioning or expiring objects.

Cross-region replication improves disaster recovery capability.

---

# 4. Database Decisions

## RDS PostgreSQL vs Aurora

### Decision

Amazon RDS PostgreSQL was selected instead of Aurora PostgreSQL.

### Rationale

LogiHaul requires relational database capabilities for transactional workloads including:

- Order records
- Driver assignments
- Billing information
- Delivery records

Aurora provides:

- Higher throughput
- Distributed storage
- Faster failover capabilities

However, RDS PostgreSQL provides the required relational database functionality at lower operational cost.

For the current deployment stage, RDS provides the best balance between reliability, functionality, and budget constraints.

As transaction volume increases, Aurora can be evaluated for higher-scale workloads.

---

# Single-AZ RDS and Read Replica Strategy

## Decision

A Single-AZ Amazon RDS PostgreSQL deployment was selected for the primary database, with a Read Replica introduced to improve read scalability.

## Rationale

The primary database handles transactional write operations where consistency is important.

The Read Replica supports read-heavy workloads such as:

- Viewing delivery status
- Order history
- Reporting queries

A Multi-AZ deployment would provide stronger availability through automatic failover and is preferred for production environments where delivery operations require minimal downtime.

However, the initial implementation prioritizes cost efficiency while still addressing scalability requirements through read replication.

The Read Replica reduces database pressure by distributing read requests away from the primary database.

As LogiHaul grows, Multi-AZ deployment can be introduced alongside additional replicas to provide both high availability and improved throughput.

---

# Redis Cache

## Decision

Redis was introduced as a caching layer.

## Rationale

Redis improves application performance by reducing repeated database queries.

The application follows a cache-aside strategy:

1. Application checks Redis.
2. Cache hit → return cached data.
3. Cache miss → query RDS.
4. Store result in Redis.

This reduces database load and improves response times during high traffic periods.

---

# 5. Serverless & Event Decisions

## Lambda Separation

### Decision

Two Lambda functions were implemented instead of combining responsibilities into one function.

### Rationale

The functions follow the Single Responsibility Principle.

### Lambda 1 — Order Processor

Responsibilities:

- Receives orders from API Gateway
- Validates requests
- Writes order data to DynamoDB
- Sends notification tasks to SQS

### Lambda 2 — Notification Processor

Responsibilities:

- Consumes messages from SQS
- Formats notification data
- Publishes notifications through SNS

Separating the functions improves scalability, reliability, and fault isolation.

During traffic spikes, order processing can continue even if notification processing slows down.

---

# SQS Decoupling Strategy

## Decision

Amazon SQS was introduced between order processing and notification processing.

## Rationale

Direct Lambda-to-Lambda communication would tightly couple the services.

Using SQS provides:

- Message durability
- Retry capability
- Fault isolation
- Asynchronous processing

If notification delivery fails, order processing is not affected.

---

# Visibility Timeout

## Decision

30 seconds.

## Rationale

Lambda 2 performs a lightweight workload:

- Reading messages
- Formatting notification payloads
- Publishing messages to SNS

The visibility timeout is longer than the expected execution duration, preventing duplicate processing while allowing failed messages to return to the queue for retry.

---

# 6. Observability Decisions

## CloudWatch Monitoring

### Decision

Centralized monitoring using Amazon CloudWatch.

### Rationale

CloudWatch provides visibility into:

- Lambda execution
- API Gateway requests
- EC2 performance
- DynamoDB activity
- ALB health

Dashboards provide operational visibility while alarms enable proactive issue detection.

CloudWatch Logs and Logs Insights support troubleshooting, debugging, and performance analysis.

---

# Final Architectural Philosophy

The LogiHaul architecture follows three core principles.

## Secure by Design

- Private workloads
- Least privilege IAM
- Controlled network access

## Scalable by Design

- Auto Scaling
- Serverless workloads
- Asynchronous messaging

## Cost-Conscious by Design

- Managed services
- Right-sized resources
- Justified architectural trade-offs

The architecture intentionally balances current business constraints with future production scalability.