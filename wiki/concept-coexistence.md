---
tags: [concept, migration]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_coexistence.md
last_updated: 2026-04-21
---

# Coexistence

Coexistence refers to the strategy of operating Vault Core alongside an existing legacy banking core during a migration. Rather than a risky "big bang" migration, banks often transition incrementally, managing both cores simultaneously.

## Key Components

A successful coexistence architecture involves several shared and distinct systems:
- **Business Process Orchestration (BPO)**: Manages end-to-end customer journeys across cores.
- **Payments Engine**: Connects to payment networks and routes messages to the correct core based on an account look-up table.
- **Domain APIs**: Stateless facades that route BPO requests to the appropriate ledger.
- **Online Data Hub**: A read-optimized, real-time repository fed by streaming APIs to support unified cross-core customer experiences.
- **Migration Pipeline**: Extract, Transform, Load (ETL) services that migrate legacy data to Vault Core in phases.
- **Customer System of Record (CSoR)**: Master view of customer data (e.g., Single Customer View) independent of the product cores.
- **Offline Data Hub**: Curated analytical store used for consolidated batch reporting and statements.

> **Diagram Summary**: A standard coexistence architecture is layered into four tiers:
> - **User Experience (UX)**: Digital, Branch & Telephony, and Operations & Support channels.
> - **Integration & Orchestration (I&O)**: Business Process Orchestration directing Domain APIs and a Payments Engine.
> - **Cores & Services**: Vault Core (Core, Posting, Streaming, and Migration APIs) runs parallel to the Legacy Core and Customer System of Record. These are bridged by Migration services and an Online Data Hub.
> - **Reporting**: An Offline Data Hub consumes data from all systems to generate Statements, Reconciliations, and Financial Reporting.

## Coexistence Patterns

There are multiple architectural patterns to manage the interaction between the legacy core and Vault Core:

1. **Mediator**: A lightweight routing service directs traffic to the correct core. The two cores do not communicate directly.
2. **Consolidated Reporting**: Both cores feed an Offline Data Hub to provide unified financial and regulatory reporting.
3. **Mirror Vault Core Through Legacy Core**: Vault Core acts as the sub-ledger, streaming real-time state changes to shadow accounts in the legacy core for downstream reporting.
4. **Moving Funds Across Cores**: Orchestrated transfers between accounts on different cores via the Payments Engine, requiring complex handling of cross-core failure scenarios.
5. **E2E Product Process Execution Across Cores**: Product features are split; Vault Core handles innovative behavior while the legacy core acts as the final system of record.

## Migration Strategy

Coexistence enables an iterative migration:
- Avoids big-bang risks.
- Acts as a strategic enabler for M&A integration.
- Requires upfront investment in automated pipelines and cross-core reconciliations.

## See Also
- [[entity-vault-core]]: The target state core banking system.
- [[concept-architecture]]: How Vault Core integrates into the broader enterprise architecture.
