---
tags: [concept, business-logic]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_what_is_vault_core.md
last_updated: 2026-04-21
---

# Smart Contracts

Smart Contracts in Vault Core encapsulate the business logic of a customer account. They represent the terms and conditions of a product and contain the logic to accept or reject postings.

## Parameterisation

Smart contracts can represent a wide range of product behaviors using parameterisation. Parameters allow a single contract to encapsulate accounts with shared but customizable functionality (e.g., an interest-only vs. capital repayment mortgage).

Parameters have a time-series representation and can be defined at multiple levels:
- **Global**: Single global value (e.g., Bank of England base rate).
- **Template**: Set across all contracts of a specific type.
- **Instance**: Specific to a single customer's account.

## Hooks and Lifecycle

Hooks are used to define the logic executed when a certain event occurs during the lifecycle of an account. The typical account lifecycle moves from Activation → Operational → Maintenance → Closure.

Key hooks include:
- **Activation**: Called before activation to schedule definitions and perform initial movements.
- **Pre-posting**: Evaluates whether to accept or reject an incoming posting.
- **Post-posting**: Runs after a posting is accepted, potentially generating additional movements or events.
- **Scheduled event**: Runs at defined frequencies (e.g., interest accruals, fee applications).
- **Conversion**: Handles converting the account to a new product version.
- **Pre/Post-parameter**: Runs when instance parameters are updated to validate or execute required actions.
- **Derived parameters**: Computes values when requested.
- **Deactivation**: Actions run during account closure.

## Schedules

Schedules execute operations on a regular cadence, such as daily interest calculations or monthly fee applications. The initial schedule cadence is defined at contract activation but can be altered throughout the account's life.

## See Also
- [[entity-vault-core]]: The overarching core banking system.
- [[concept-postings]]: How Smart Contracts interact with fund movements.
- [[concept-financial-model]]: How scheduled events and postings dictate the financial model.
