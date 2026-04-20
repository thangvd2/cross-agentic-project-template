---
tags: [concept, architecture]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_architecture.md
last_updated: 2026-04-21
---

# Architecture

Vault Core is a cloud-native core banking engine built using a microservices architecture and deployed on Kubernetes. This approach enables dynamic scaling, resilience, and high availability.

## Scaling

Vault Core supports horizontal and elastic scaling to meet modern banking workloads:
- **Stateless Microservices**: Scaled automatically using Kubernetes Horizontal Pod Autoscalers (HPAs) based on CPU, memory, and custom metrics (e.g., gRPC requests per second).
- **Postgres Database**: Storage scales as data grows, with zero downtime storage autoscaling.
- **Kafka Streaming**: Provides event-driven, real-time messaging. It scales writes to achieve high throughput and decouples batch processing load from online transactions.

## High Availability and Resilience

Vault Core ensures high availability (HA) and disaster recovery (DR) by deploying its critical components across three fault domains (on-premise) or availability zones (public cloud):
- **Kubernetes**: Control plane and data plane (microservices) span three zones.
- **Postgres**: Uses logical database replication with a master and hot standby across zones for zero data loss and rapid failover.
- **Kafka**: Active-active-active broker setup across three zones, with synchronous topic replication.

## Security Overview

The architecture incorporates robust security measures:
- **Data Encryption**: All transit is encrypted via TLS. At rest, data is encrypted via AES-256 (with optional Customer Managed Keys for bank-hosted instances).
- **Authentication**: Utilizes SAML for the UI, JWT for APIs, and mTLS/ACLs/SASL for Kafka streaming.

## Legacy vs. Modern Architecture

Unlike legacy monolithic architectures that process steps in a single database under a single unit of work, Vault Core processes user journeys concurrently across microservices. This allows performance to be decoupled from simple database reads/writes and tied directly to user journey execution.

## See Also
- [[entity-vault-core]]: Overview of the Vault Core platform.
- [[concept-security]]: Deep dive into Vault Core's security model.
