# LogiHaul Cloud Architecture

## Problem Statement

LogiHaul is a pan-Nigeria logistics platform that connects customers with over 5,000 truck drivers operating across all 36 states and the Federal Capital Territory. The platform enables customers to place delivery requests, matches them with available drivers, tracks deliveries in real time, processes billing, and keeps customers informed through timely delivery notifications.

As the business grows, the platform faces several architectural challenges. Customer demand is highly unpredictable, with traffic increasing by as much as 50 times during promotional campaigns, festive seasons, and emergency situations such as flooding. The infrastructure must therefore scale automatically to accommodate sudden spikes in traffic without degrading user experience.

In addition to scalability, the platform requires high availability. Delivery operations are business-critical, meaning downtime can directly affect customers, drivers, and revenue. The system must continue operating even if an Availability Zone becomes unavailable while ensuring that customer orders are not lost during failures.

The platform also requires low-latency processing. Customers expect order confirmations and delivery updates within seconds, while backend services must process requests efficiently without introducing unnecessary delays. At the same time, the solution must remain cost-effective since infrastructure expenses must align with the company's current operational budget while allowing room for future growth.

To address these challenges, this project designs and implements a secure, scalable, event-driven cloud architecture on Amazon Web Services (AWS) that balances reliability, performance, security and cost optimization.

---

# Solution Overview

The proposed solution adopts a hybrid cloud architecture that combines traditional compute resources with serverless services. Rather than relying exclusively on either virtual machines or serverless computing, the architecture assigns each workload to the platform best suited for its operational characteristics.

The traditional compute layer supports the core web application responsible for serving users, managing application logic, and interacting with relational data stores. The serverless layer complements this by handling event-driven workloads such as order processing and customer notifications. This separation of responsibilities improves scalability, simplifies maintenance, and ensures that long-running application processes do not delay asynchronous background operations.

The architecture was designed around six foundational layers:

* Foundation & Identity
* Compute & Scaling
* Storage
* Databases
* Serverless & Event Processing
* Observability

Each layer addresses a specific business requirement while collectively providing a secure, resilient and scalable platform capable of supporting nationwide logistics operations.

---

# Architecture Objectives

The solution was designed to achieve the following objectives:

* Provide secure network isolation through a custom Virtual Private Cloud.
* Support automatic scaling during sudden traffic surges.
* Protect critical business data through private database deployments and encryption.
* Process customer orders reliably using asynchronous event-driven workflows.
* Deliver customer notifications without affecting order processing performance.
* Improve application responsiveness through intelligent caching.
* Provide centralized monitoring, logging and alerting for operational visibility.
* Maintain a cost-conscious architecture while preserving a clear path toward future production-scale enhancements.

The following sections describe each architectural layer, the AWS services selected, the design decisions made, and the trade-offs considered during implementation.

---

# Architecture Layers

The LogiHaul cloud architecture is organized into six major layers, with each layer responsible for a specific part of the platform's operation. This layered approach ensures that the system remains secure, scalable, reliable, and cost-efficient while supporting the requirements of a nationwide logistics platform.

![LogiHaul Architecture Diagram](architecture/Full Architecture.pdf)

The architecture combines traditional infrastructure and serverless services to handle customer requests, process delivery operations, store application data, manage events, and monitor system performance.

The six architectural layers are:

Foundation & Identity — Provides the secure network foundation through VPC design, subnet segmentation, security groups, and IAM roles following least-privilege principles.
Compute & Scaling — Handles application hosting through Amazon EC2, Application Load Balancer, and Auto Scaling to support variable traffic and sudden demand increases.
Storage — Provides scalable object storage through Amazon S3 with features such as encryption, versioning, lifecycle management, and cross-region replication.
Databases — Manages application data using Amazon RDS PostgreSQL for transactional workloads, ElastiCache Redis for performance optimization, and DynamoDB for event-driven workloads.
Serverless & Events — Enables asynchronous processing through API Gateway, Lambda, SQS, and SNS, allowing order processing and notification workflows to scale independently.
Observability — Provides monitoring, logging, dashboards, and alerting through Amazon CloudWatch to support operational visibility and faster troubleshooting.

Together, these layers create a cloud architecture that balances current business constraints with future scalability requirements while supporting LogiHaul's goal of reliable nationwide delivery operations.