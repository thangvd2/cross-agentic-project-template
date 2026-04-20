---
tags: [entity, core-banking]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_what_is_vault_core.md
  - raw/vault-core-overview/vault_core_overview.md
last_updated: 2026-04-21
---

# Vault Core

Vault Core is Thought Machine's next-generation, cloud-native core banking system. It provides a real-time, append-only ledger that maintains the current state of customer (external) accounts and bank (internal) accounts.

## Conceptual Model

The conceptual model of Vault Core relies on three main pillars:
1. **Smart Contracts**: The business logic of the account. They dictate whether posting instructions (fund movements) are accepted or rejected based on the contract's defined rules.
2. **Vault Core APIs & Ledger**: The underlying system that processes accepted postings to update account balances across multiple dimensions (e.g., asset classes, denominations, addresses, phases).
3. **Streaming Events**: All state changes within Vault Core are provided as a stream of events, allowing external systems to consume real-time updates asynchronously.

> **Diagram Summary**: The conceptual model visualizes Vault Core APIs as the central layer, bridging Smart Contracts above and the Ledger below. It highlights the primary data flows: Core commands and Migrations feed into the system, while Postings and Streaming events flow out.

Vault Core is fundamentally designed to be highly available and to scale dynamically to meet short-term spikes and long-term growth through a distributed, cloud-based infrastructure.

## Core Capabilities

- **Real-Time Append-Only Ledger**: The ledger consists of an ordered series of accepted fund movements. Balances are derived from these movements in real time.
- **Cloud-Native & Highly Available**: Built as a distributed microservices system on Kubernetes, ensuring seamless scaling and high availability across multiple zones.
- **Streaming Events**: Instead of relying on polling or ad hoc queries, downstream systems consume real-time state changes directly from Kafka topics.

## See Also

- [[concept-architecture]]: Details on the Kubernetes-based microservices architecture, scaling, and high availability.
- [[concept-financial-model]]: How Vault Core derives balances and handles End of Day (EOD) processes.
- [[concept-security]]: The shared responsibility model and data protection standards within Vault Core.
- [[concept-postings]]: The fundamental mechanism for moving funds between accounts.
- [[concept-smart-contracts]]: How account logic is encapsulated and parameterized.
- [[concept-coexistence]]: Strategies for running Vault Core alongside legacy core systems.
- [[ref-vc5-service-compatibility]]: Compatibility and upgrade paths for Vault Core 5 services.
