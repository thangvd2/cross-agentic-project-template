---
tags: [reference, versioning]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_whats_new_in_vc5_service_compatibility.md
last_updated: 2026-04-21
---

# VC5 Service Compatibility

Vault Core 5 introduces several major architectural shifts, including a v2 Accounts API, CLv4 Smart Contracts, new Parameters resources, Processing Groups, and Adjustments. This page details their compatibility matrices and required upgrade paths.

## Service Compatibility Matrix

The following table summarizes the compatibility of services introduced in Vault Core 5:

| Accounts version | Smart Contract Language version | Core API Parameters resource | Processing Groups | Adjustments |
| --- | --- | --- | --- | --- |
| /v1/accounts | CLv3 | NO | NO | NO |
| /v1/accounts | CLv4 | NO | YES | NO |
| /v2/accounts | CLv4 | YES | YES | YES |

> **NOTE**: Supervisor Contracts are not currently compatible with Core API Parameters or Adjustments.

## Accounts and Contract Language Compatibility

| Vault Core Version | Contract Language version | Accounts v1 | Accounts v2 | Notes |
| --- | --- | --- | --- | --- |
| 4.6/4.7 | v3, v4 | YES | N/A | Contract Language v4 live |
| 5.X | v3 | YES | NO | Accounts v2 live |
| 5.X | v4 | YES | YES | |
| 6.X | v3 | NO | NO | Contracts Language v3 no longer supported |
| 6.X | v4 | PARTIAL | YES | Accounts v1 endpoint remains only to support updates of CLv4 Accounts |
| 7.X | v3 | N/A | NO | Accounts v1 removed no earlier than this version. |
| 7.X | v4 | N/A | YES | |

## Required Switch Order

To safely transition and receive all Vault Core 5 benefits, services must be upgraded in the following exact order:

1. **Upgrade Contracts**: Upgrade all Smart Contracts and Supervisor Contracts to CLv4.
2. **Configure Timezones**: Activate the default Processing Group timezone (if requiring a single timezone).
3. **Switch Accounts API**: Migrate integrations from the v1 to the v2 Accounts API.
4. **Switch Parameters API**: Migrate from Smart Contract Global/Instance parameters to the new Core API Parameters resource.

*Once step 4 is completed, the Adjustments extension can be utilized.*

## See Also
- [[entity-vault-core]]: The overarching core banking system.
