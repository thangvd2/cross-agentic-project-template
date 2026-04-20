---
tags: [source, overview]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_what_is_vault_core.md
  - raw/vault-core-overview/vault_core_overview_architecture.md
  - raw/vault-core-overview/vault_core_overview_financial_model.md
  - raw/vault-core-overview/vault_core_overview_vault_security.md
  - raw/vault-core-overview/vault_core_overview_coexistence.md
  - raw/vault-core-overview/vault_core_overview_whats_new_in_vc5.md
  - raw/vault-core-overview/vault_core_overview_whats_new_in_vc5_overview.md
  - raw/vault-core-overview/vault_core_overview_whats_new_in_vc5_service_compatibility.md
  - raw/vault-core-overview/vault_core_overview_whats_new_in_vc5_extensions.md
  - raw/vault-core-overview/vault_core_overview.md
last_updated: 2026-04-21
---

# Vault Core Overview Sources

This page provides a structured summary of the raw documents that comprise the Vault Core Overview.

## What is Vault Core?
Vault Core is a cloud-native, real-time core banking system. It maintains a ledger of accepted postings (fund movements) across various balance dimensions (asset classes, denominations, addresses, phases). Account logic is dictated by Smart Contracts which use hooks, parameters, and schedules to process account lifecycles. All state changes are emitted as streaming events.
- **Extracted concepts**: [[entity-vault-core]], [[concept-postings]], [[concept-smart-contracts]]

## Architecture
Vault Core's distributed microservices architecture runs on Kubernetes across multiple availability zones. It uses Postgres for database storage and Kafka for asynchronous streaming. The architecture prioritizes horizontal scalability, high availability, and disaster recovery.
- **Extracted concepts**: [[concept-architecture]]

## Financial Model
The financial model relies on postings to derive balances. Vault Core distinguishes between being the source of truth vs. a system of record. End of Day (EOD) processing utilizes the 1º and 2º cut-off times to determine which day overnight postings belong to, allowing the system to arrive at consistent EOD positions.
- **Extracted concepts**: [[concept-financial-model]]

## Coexistence
Banks migrating to Vault Core often employ coexistence strategies alongside their legacy cores. This involves components like Business Process Orchestration, Domain APIs, Payments Engines, and Offline/Online Data Hubs. Various coexistence patterns (e.g., Mediator, Consolidated Reporting, Mirroring) dictate how the cores interact.
- **Extracted concepts**: [[concept-coexistence]]

## Security
Vault Core relies on a shared responsibility model. It adheres to strict compliance certifications (ISO 27001/22301, SOC 2). Security is integrated into the SDLC (threat modeling, scanning), and the platform mandates TLS encryption in transit, AES 256 at rest, and JWT/SAML-based authentication.
- **Extracted concepts**: [[concept-security]]

## What's New in VC5 — Overview
Vault Core 5 introduces major improvements, such as the synchronous v2 Accounts API, independent Parameters APIs decoupled from Smart Contracts, and enhanced deterministic EOD capabilities via effective time fetching. It also brings timezone-aware Processing Groups.
- **Extracted concepts**: [[entity-vault-core]], [[ref-vc5-service-compatibility]]

## What's New in VC5 — Service Compatibility
Upgrading to Vault Core 5 requires a specific sequence: migrating Smart Contracts to CLv4, configuring Processing Group timezones, adopting the v2 Accounts API, and switching to the new Core API Parameters resource. Adjustments can only be used after this switch.
- **Extracted concepts**: [[ref-vc5-service-compatibility]]

## What's New in VC5 — Extensions
Vault Core 5 offers extensions such as Multiple Processing Groups for operational isolation, High-volume Accounts for large-scale operations, Hibernator for cost-saving on non-production instances, and Adjustments for retroactive balance correction.
- **Extracted concepts**: [[entity-vault-core]]
